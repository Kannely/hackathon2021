import json

from django.http import HttpResponse, JsonResponse

import urllib.request
from urllib.error import HTTPError
from .models import *
from django.forms.models import model_to_dict

PASS_PREFIX = "/pass/"


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. This is the back-end !")


def __get_pass_url__(request, suffix):
    return request.build_absolute_uri(PASS_PREFIX + suffix)


def __make_json_request__(request, url, transfer_cookie=True, fields_only=False):
    cookie = request.headers.get("Cookie")
    new_request = urllib.request.Request(url)
    if transfer_cookie and cookie:
        new_request.add_header("Cookie", cookie)
    try:
        url = urllib.request.urlopen(new_request)
        data = json.loads(url.read().decode())
        if fields_only:
            data = data[0]['fields']
        return data, 200
    except HTTPError as err:
        return {}, err.code


def get_synthesis(request):
    url = __get_pass_url__(request, 'etudiant')
    etudiant_data, etudiant_code = __make_json_request__(request, url, fields_only=True)
    if etudiant_code == 200:
        for taf in ['tafA2', 'tafA3']:
            if etudiant_data[taf] is None:
                etudiant_data[taf] = '-'
            else:
                taf_url = __get_pass_url__(request, 'taf/' + str(etudiant_data[taf]))
                taf_data, taf_code = __make_json_request__(request, taf_url, fields_only=True)
                if taf_code == 200:
                    etudiant_data[taf] = taf_data['code']

        formation_url = __get_pass_url__(request, 'formation/' + str(etudiant_data['formation']))
        formation_data, formation_code = __make_json_request__(request, formation_url, fields_only=True)
        if formation_code == 200:
            etudiant_data['formation'] = formation_data['code']

        periode_url = __get_pass_url__(request, 'periode/' + str(etudiant_data['periode_actuelle']))
        periode_data, periode_code = __make_json_request__(request, periode_url, fields_only=True)
        if periode_code == 200:
            etudiant_data['formation'] = etudiant_data['formation'] + periode_data['code'][:2]

        del etudiant_data['obligations']
        del etudiant_data['ues']
        del etudiant_data['periode_actuelle']
    return JsonResponse(etudiant_data, status=etudiant_code)


def get_suivre_ue(request, periode=None):
    url = __get_pass_url__(request, 'etudiant')
    etudiant_data, etudiant_code = __make_json_request__(request, url, fields_only=True)
    all_suivre_ues = []
    if etudiant_code == 200:
        for id in etudiant_data['ues']:
            suivre_ue_url = __get_pass_url__(request, 'ue_suivi/' + str(id))
            suivre_ue_data, suivre_ue_code = __make_json_request__(request, suivre_ue_url, fields_only=True)
            if suivre_ue_code == 200:
                if periode is None:
                    all_suivre_ues.append(suivre_ue_data)
                else:
                    periode_url = __get_pass_url__(request, 'periode/' + str(suivre_ue_data['periode']))
                    periode_data, periode_code = __make_json_request__(request, periode_url, fields_only=True)
                    if periode_code == 200 and (periode_data['code'].find(periode) != -1):
                        all_suivre_ues.append(suivre_ue_data)
    return all_suivre_ues


def get_eval_competences(request, periode=None):
    ues = get_suivre_ue(request, periode)
    competences = []
    for ue in ues:
        competences += ue['competences']
    all_eval_comp = []
    for ec in set(competences):
        eval_competence_url = __get_pass_url__(request, 'eval_competence/' + str(ec))
        eval_comp_data, eval_comp_code = __make_json_request__(request, eval_competence_url, fields_only=True)
        if eval_comp_code == 200:
            all_eval_comp.append(eval_comp_data)
        else:
            return None  # TODO
    return all_eval_comp


def get_bilan_competence(request, periode=None):
    evals = get_eval_competences(request, periode)
    default = {'win': 0, 'loose': 0}
    bilan = {}
    for e in evals:
        if e["competence"] not in bilan.keys():
            bilan[e["competence"]] = {}
            for i in range(1, 6):
                bilan[e["competence"]][i] = default.copy()
        if e["jetons_valides"] is not None:
            if e["jetons_valides"] == 0:
                bilan[e["competence"]][e["niveau"]]['loose'] += e["jetons_tentes"]
            else:
                bilan[e["competence"]][e["niveau"]]['win'] += e["jetons_valides"]
    return bilan


def get_niveau_competences(request):
    bilan = get_bilan_competence(request)
    niveaux = {}
    for c in bilan.keys():
        comp_url = __get_pass_url__(request, 'competence/' + str(c))
        comp_data, comp_code = __make_json_request__(request, comp_url, fields_only=True)
        if comp_code == 200:
            niveau = 0
            seuil = 1
            while seuil < 6 and bilan[c][seuil]['win'] >= comp_data['seuil' + str(seuil)]:
                niveau = seuil
                seuil += 1
            niveaux[comp_data['code']] = niveau
    return niveaux


def get_comp_gen(request):
    niveau_dict = get_niveau_competences(request)
    gen_dict = niveau_dict.copy()
    for key in niveau_dict.keys():
        if key[:2] != 'CG':
            del gen_dict[key]
    return JsonResponse(gen_dict, status=200)


def get_ue_per_year(request):
    ues = get_suivre_ue(request)
    ue_per_year = {'A1': {'valide': 0, 'tente': 0}, 'A2': {'valide': 0, 'tente': 0}, 'A3': {'valide': 0, 'tente': 0}}
    for ue in ues:
        periode_url = __get_pass_url__(request, 'periode/' + str(ue['periode']))
        periode_data, periode_code = __make_json_request__(request, periode_url, fields_only=True)
        if periode_code == 200:
            ue_per_year[periode_data['code'][:2]]['tente'] += 1
            if ue['ects_obtenus'] is not None and ue['ects_obtenus'] > 0:
                ue_per_year[periode_data['code'][:2]]['valide'] += 1
    return JsonResponse(ue_per_year, status=200)


def get_jetons(request):
    bilan = get_bilan_competence(request)
    result = {'current_year': 0, 'total': 0}
    for k in bilan.keys():
        for l in bilan[k].keys():
            result['total'] += bilan[k][l]['win']

    url = __get_pass_url__(request, 'etudiant')
    etudiant_data, etudiant_code = __make_json_request__(request, url, fields_only=True)
    if etudiant_code == 200:
        periode_url = __get_pass_url__(request, 'periode/' + str(etudiant_data['periode_actuelle']))
        periode_data, periode_code = __make_json_request__(request, periode_url, fields_only=True)
        if periode_code == 200:
            year = get_bilan_competence(request, periode=periode_data['code'][:2])
            for k in year.keys():
                for l in year[k].keys():
                    result['current_year'] += year[k][l]['win']
    return JsonResponse(result, status=200)


def get_ects(request):
    ues = get_suivre_ue(request)
    result = {'current_year': 0, 'total': 0}
    for ue in ues:
        result['total'] += ue['ects_obtenus']
    url = __get_pass_url__(request, 'etudiant')
    etudiant_data, etudiant_code = __make_json_request__(request, url, fields_only=True)
    if etudiant_code == 200:
        periode_url = __get_pass_url__(request, 'periode/' + str(etudiant_data['periode_actuelle']))
        periode_data, periode_code = __make_json_request__(request, periode_url, fields_only=True)
        if periode_code == 200:
            year = get_suivre_ue(request, periode=periode_data['code'][:2])
            for ue in year:
                result['current_year'] += ue['ects_obtenus']
    return JsonResponse(result, status=200)


def get_obligations(request):
    url = __get_pass_url__(request, 'etudiant')
    etudiant_data, etudiant_code = __make_json_request__(request, url, fields_only=True)
    if etudiant_code == 200:
        url = __get_pass_url__(request, 'obligation/' + str(etudiant_data['obligations']))
        obl_data, obl_code = __make_json_request__(request, url, fields_only=True)
        formation_url = __get_pass_url__(request, 'formation/' + str(etudiant_data['formation']))
        formation_data, formation_code = __make_json_request__(request, formation_url, fields_only=True)
        if formation_code == 200:
            obj = Obligations.objects.filter(formation=formation_data['code']).first()
            obj = model_to_dict(obj)
            result = {'etudiant': obl_data, 'formation': obj}
            return JsonResponse(result, status=200, safe=False)
