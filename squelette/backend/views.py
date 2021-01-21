from django.http import HttpResponse, JsonResponse
from django.conf import settings

import json

import urllib.request
from urllib.error import HTTPError
from .models import *
from django.forms.models import model_to_dict

lv_dict = {
    'A1': 1,
    'A2': 2,
    'B1': 3,
    'B2': 4,
    'C1': 5,
    'C2': 6
}

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. This is the back-end !")


def __get_pass_url__(request, suffix):
    return request.build_absolute_uri(settings.PASS_PREFIX + suffix)


def __make_json_request__(request, url, transfer_cookie=True, fields_only=False):
    cookie = request.headers.get("Cookie")
    new_request = urllib.request.Request(url)
    if transfer_cookie and cookie:
        new_request.add_header("Cookie", cookie)
    try:
        response = urllib.request.urlopen(new_request)
        data = json.loads(response.read().decode())
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


def __get_suivre_ue__(request, periode=None):
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
    ues = __get_suivre_ue__(request, periode)
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


def __get_bilan_competence__(request, periode=None):
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


def __get_niveau_competences__(request):
    bilan = __get_bilan_competence__(request)
    lvls = {}
    for c in bilan.keys():
        comp_url = __get_pass_url__(request, 'competence/' + str(c))
        comp_data, comp_code = __make_json_request__(request, comp_url, fields_only=True)
        if comp_code == 200:
            niveau = 0
            for seuil in range(1, 6):
                if bilan[c][seuil]['win'] >= comp_data['seuil' + str(seuil)]:
                    niveau = seuil
            lvls[comp_data['code']] = niveau
    return lvls


def get_comp_gen(request):
    niveau_dict = __get_niveau_competences__(request)
    gen_dict = niveau_dict.copy()
    for key in niveau_dict.keys():
        if key[:2] != 'CG':
            del gen_dict[key]
    return JsonResponse(gen_dict, status=200)


def get_ue_per_year(request):
    ues = __get_suivre_ue__(request)
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
    bilan = __get_bilan_competence__(request)
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
            year = __get_bilan_competence__(request, periode=periode_data['code'][:2])
            for k in year.keys():
                for l in year[k].keys():
                    result['current_year'] += year[k][l]['win']
    return JsonResponse(result, status=200)


def get_ects(request):
    ues = __get_suivre_ue__(request)
    result = {'current_year': 0, 'total': 0}
    for ue in ues:
        result['total'] += ue['ects_obtenus'] if ue['ects_obtenus'] is not None else 0
    url = __get_pass_url__(request, 'etudiant')
    etudiant_data, etudiant_code = __make_json_request__(request, url, fields_only=True)
    if etudiant_code == 200:
        periode_url = __get_pass_url__(request, 'periode/' + str(etudiant_data['periode_actuelle']))
        periode_data, periode_code = __make_json_request__(request, periode_url, fields_only=True)
        if periode_code == 200:
            year = __get_suivre_ue__(request, periode=periode_data['code'][:2])
            for ue in year:
                result['current_year'] += ue['ects_obtenus'] if ue['ects_obtenus'] is not None else 0
    return JsonResponse(result, status=200)


def get_obligations(request):
    url = __get_pass_url__(request, 'etudiant')
    etudiant_data, etudiant_code = __make_json_request__(request, url, fields_only=True)
    if etudiant_code == 200:
        url = __get_pass_url__(request, 'obligation/' + str(etudiant_data['obligations']))
        obl_data, obl_code = __make_json_request__(request, url, fields_only=True)
        obl_data['ects'] = 0
        ues = __get_suivre_ue__(request)
        for ue in ues:
            obl_data['ects'] += ue['ects_obtenus'] if ue['ects_obtenus'] is not None else 0
        obl_data['c2io'] = 0
        for ue in ues:
            url = __get_pass_url__(request, 'ue/' + str(ue['ue']))
            ue_data, ue_code = __make_json_request__(request, url, fields_only=True)
            if ue_code == 200:
                if ue_data["c2io"]:
                    obl_data['c2io'] += ue['ects_obtenus']
        obl_data['comp_nv3'] = 0
        niveau_dict = __get_niveau_competences__(request)
        for k in niveau_dict.keys():
            if k[:2] == 'CG' and niveau_dict[k] > 0:
                obl_data['comp_nv3'] += 1
        formation_url = __get_pass_url__(request, 'formation/' + str(etudiant_data['formation']))
        formation_data, formation_code = __make_json_request__(request, formation_url, fields_only=True)
        if formation_code == 200:
            obj = Obligations.objects.filter(formation=formation_data['code']).first()
            obj = model_to_dict(obj)
            del obj['id']
            del obj['formation']
            result = {'etudiant': obl_data, 'formation': obj, "percentage": 0}
            result['percentage'] += min(1.0, result['etudiant']['stage'] / result['formation']['stage'])
            result['percentage'] += min(1.0, result['etudiant']['etranger'] / result['formation']['etranger'])
            result['percentage'] += min(1.0, float(result['etudiant']['ielts']) / float(result['formation']['ielts']))
            result['percentage'] += min(1.0, lv_dict[result['etudiant']['lv1']] / lv_dict[result['formation']['lv1']])
            result['percentage'] += min(1.0, lv_dict[result['etudiant']['lv2']] / lv_dict[result['formation']['lv2']])
            result['percentage'] += min(1.0, result['etudiant']['ects'] / result['formation']['ects'])
            result['percentage'] += min(1.0, result['etudiant']['c2io'] / result['formation']['c2io'])
            result['percentage'] += min(1.0, result['etudiant']['comp_nv3'] / result['formation']['comp_nv3'])
            result['percentage'] = result['percentage'] / 8
            return JsonResponse(result, status=200, safe=False)


def all_ue(request):
    url = __get_pass_url__(request, 'etudiant')
    etudiant_data, _ = __make_json_request__(request, url, fields_only=True)
    p = etudiant_data['periode_actuelle']
    ue_suivi = __get_suivre_ue__(request)
    termine_list = set()
    en_cours_list = set()
    for ue in ue_suivi:
        if ue['periode'] == p:
            en_cours_list.add(ue['ue'])
        else:
            termine_list.add(ue['ue'])
    url = __get_pass_url__(request, 'all_ue')
    ues_data, ues_code = __make_json_request__(request, url, fields_only=False)
    result = []
    if ues_code == 200:
        for ue in ues_data:
            pk = ue['pk']
            fields = ue['fields']
            infos = {'id':pk, 'code': fields['code'], 'creneau': fields['creneau'], 'termine': pk in termine_list,
                     'en_cours': pk in en_cours_list}
            result.append(infos)
        return JsonResponse(result, status=200, safe=False)


def all_competence(request):
    pass
