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
    if settings.PASS_URL:
        return settings.PASS_URL + suffix
    else:
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
    if etudiant_code != 200:
        return JsonResponse(etudiant_data, status=etudiant_code)
    for taf in ['tafA2', 'tafA3']:
        if etudiant_data[taf] is None:
            etudiant_data[taf] = '-'
        else:
            taf_url = __get_pass_url__(request, 'taf/' + str(etudiant_data[taf]))
            taf_data, taf_code = __make_json_request__(request, taf_url, fields_only=True)
            if taf_code != 200:
                return JsonResponse(taf_data, status=taf_code)
            etudiant_data[taf] = taf_data['code']

    formation_url = __get_pass_url__(request, 'formation/' + str(etudiant_data['formation']))
    formation_data, formation_code = __make_json_request__(request, formation_url, fields_only=True)
    if formation_code != 200:
        return JsonResponse(formation_data, status=formation_code)
    etudiant_data['formation'] = formation_data['code']

    periode_url = __get_pass_url__(request, 'periode/' + str(etudiant_data['periode_actuelle']))
    periode_data, periode_code = __make_json_request__(request, periode_url, fields_only=True)
    if periode_code != 200:
        return JsonResponse(periode_data, status=periode_code)
    etudiant_data['formation'] = etudiant_data['formation'] + periode_data['code'][:2]

    del etudiant_data['obligations']
    del etudiant_data['ues']
    del etudiant_data['periode_actuelle']
    return JsonResponse(etudiant_data)


def __get_suivre_ue__(request, periode=None):
    url = __get_pass_url__(request, 'etudiant')
    etudiant_data, etudiant_code = __make_json_request__(request, url, fields_only=True)
    all_suivre_ues = []
    if etudiant_code != 200:
        return None
    for ue_id in etudiant_data['ues']:
        suivre_ue_url = __get_pass_url__(request, 'ue_suivi/' + str(ue_id))
        suivre_ue_data, suivre_ue_code = __make_json_request__(request, suivre_ue_url, fields_only=True)
        if suivre_ue_code != 200:
            return None
        if periode is None:
            all_suivre_ues.append(suivre_ue_data)
        else:
            periode_url = __get_pass_url__(request, 'periode/' + str(suivre_ue_data['periode']))
            periode_data, periode_code = __make_json_request__(request, periode_url, fields_only=True)
            if periode_code != 200:
                return None
            if (periode_data['code'].find(periode) != -1):
                all_suivre_ues.append(suivre_ue_data)
    return all_suivre_ues


def __get_eval_competences__(request, periode=None):
    ues = __get_suivre_ue__(request, periode)
    if ues is None:
        return None
    competences = []
    for ue in ues:
        competences += ue['competences']
    all_eval_comp = []
    for ec in set(competences):
        eval_competence_url = __get_pass_url__(request, 'eval_competence/' + str(ec))
        eval_comp_data, eval_comp_code = __make_json_request__(request, eval_competence_url, fields_only=True)
        if eval_comp_code != 200:
            return None
        all_eval_comp.append(eval_comp_data)
    return all_eval_comp


def __get_bilan_competence__(request, periode=None):
    evals = __get_eval_competences__(request, periode)
    if evals is None:
        return None
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
    if bilan is None:
        return None
    lvls = {}
    for c in bilan.keys():
        comp_url = __get_pass_url__(request, 'competence/' + str(c))
        comp_data, comp_code = __make_json_request__(request, comp_url, fields_only=True)
        if comp_code != 200:
            return None
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
    return JsonResponse(gen_dict)


def get_ue_per_year(request):
    ues = __get_suivre_ue__(request)
    ue_per_year = {'A1': {'valide': 0, 'tente': 0}, 'A2': {'valide': 0, 'tente': 0}, 'A3': {'valide': 0, 'tente': 0}}
    for ue in ues:
        periode_url = __get_pass_url__(request, 'periode/' + str(ue['periode']))
        periode_data, periode_code = __make_json_request__(request, periode_url, fields_only=True)
        if periode_code != 200:
            return JsonResponse(periode_data, status=periode_code)
        ue_per_year[periode_data['code'][:2]]['tente'] += 1
        if ue['ects_obtenus'] is not None and ue['ects_obtenus'] > 0:
            ue_per_year[periode_data['code'][:2]]['valide'] += 1
    return JsonResponse(ue_per_year)


def get_jetons(request):
    bilan = __get_bilan_competence__(request)
    result = {'current_year': 0, 'total': 0}
    for k in bilan.keys():
        for l in bilan[k].keys():
            result['total'] += bilan[k][l]['win']
    url = __get_pass_url__(request, 'etudiant')
    etudiant_data, etudiant_code = __make_json_request__(request, url, fields_only=True)
    if etudiant_code != 200:
        return JsonResponse(etudiant_data, status=etudiant_code)
    periode_url = __get_pass_url__(request, 'periode/' + str(etudiant_data['periode_actuelle']))
    periode_data, periode_code = __make_json_request__(request, periode_url, fields_only=True)
    if periode_code != 200:
        return JsonResponse(periode_data, status=periode_code)
    year = __get_bilan_competence__(request, periode=periode_data['code'][:2])
    for k in year.keys():
        for l in year[k].keys():
            result['current_year'] += year[k][l]['win']
    return JsonResponse(result)


def get_ects(request):
    ues = __get_suivre_ue__(request)
    result = {'current_year': 0, 'total': 0}
    for ue in ues:
        result['total'] += ue['ects_obtenus'] if ue['ects_obtenus'] is not None else 0
    url = __get_pass_url__(request, 'etudiant')
    etudiant_data, etudiant_code = __make_json_request__(request, url, fields_only=True)
    if etudiant_code != 200:
        return JsonResponse(etudiant_data, status=etudiant_code)
    periode_url = __get_pass_url__(request, 'periode/' + str(etudiant_data['periode_actuelle']))
    periode_data, periode_code = __make_json_request__(request, periode_url, fields_only=True)
    if periode_code != 200:
        return JsonResponse(periode_data, status=periode_code)
    year = __get_suivre_ue__(request, periode=periode_data['code'][:2])
    for ue in year:
        result['current_year'] += ue['ects_obtenus'] if ue['ects_obtenus'] is not None else 0
    return JsonResponse(result)


def get_obligations(request):
    url = __get_pass_url__(request, 'etudiant')
    etudiant_data, etudiant_code = __make_json_request__(request, url, fields_only=True)
    if etudiant_code != 200:
        return JsonResponse(etudiant_data, status=etudiant_code)
    url = __get_pass_url__(request, 'obligation/' + str(etudiant_data['obligations']))
    obl_data, obl_code = __make_json_request__(request, url, fields_only=True)
    if obl_code != 200:
        return JsonResponse(obl_data, status=obl_code)
    obl_data['ects'] = 0
    obl_data['c2io'] = 0
    obl_data['comp_nv3'] = 0
    ues = __get_suivre_ue__(request)
    for ue in ues:
        obl_data['ects'] += ue['ects_obtenus'] if ue['ects_obtenus'] is not None else 0
        url = __get_pass_url__(request, 'ue/' + str(ue['ue']))
        ue_data, ue_code = __make_json_request__(request, url, fields_only=True)
        if ue_code != 200:
            return JsonResponse(ue_data, status=ue_code)
        if ue_data["c2io"]:
            obl_data['c2io'] += ue['ects_obtenus']
    niveau_dict = __get_niveau_competences__(request)
    for k in niveau_dict.keys():
        if k[:2] == 'CG' and niveau_dict[k] > 0:
            obl_data['comp_nv3'] += 1
    formation_url = __get_pass_url__(request, 'formation/' + str(etudiant_data['formation']))
    formation_data, formation_code = __make_json_request__(request, formation_url, fields_only=True)
    if formation_code != 200:
        return JsonResponse(formation_data, status=formation_code)
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
    return JsonResponse(result, safe=False)


def all_ue(request):
    url = __get_pass_url__(request, 'etudiant')
    etudiant_data, etudiant_code = __make_json_request__(request, url, fields_only=True)
    if etudiant_code != 200:
        return JsonResponse(etudiant_data, status=etudiant_code)
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
    if ues_code != 200:
        return JsonResponse(ues_data, status=ues_code)
    for ue in ues_data:
        pk = ue['pk']
        fields = ue['fields']
        infos = {'id': pk, 'code': fields['code'], 'creneau': fields['creneau'], 'termine': pk in termine_list,
                 'en_cours': pk in en_cours_list}
        result.append(infos)
    return JsonResponse(result, safe=False)


def get_ue_details(request, pk):
    ue_suivi = __get_suivre_ue__(request)
    suivi = False
    evals = {}
    for ue in ue_suivi:
        if ue['ue'] == pk:
            suivi = True
            evals = ue
    url = __get_pass_url__(request, 'ue/' + str(pk))
    ue_data, ue_code = __make_json_request__(request, url, fields_only=True)
    if ue_code != 200:
        return JsonResponse(ue_data, status=ue_code)
    ue_data['suivi'] = suivi
    if suivi:
        periode_url = __get_pass_url__(request, 'periode/' + str(evals['periode']))
        periode_data, periode_code = __make_json_request__(request, periode_url, fields_only=True)
        if periode_code != 200:
            return JsonResponse(periode_data, periode_code)
        evals['periode'] = periode_data['code']
        del evals['ue']
        ue_data = {**ue_data, **evals}
    return JsonResponse(ue_data, safe=False)


def get_eval_comp(request, pk):
    eval_competence_url = __get_pass_url__(request, 'eval_competence/' + str(pk))
    eval_comp_data, eval_comp_code = __make_json_request__(request, eval_competence_url, fields_only=True)
    if eval_comp_code != 200:
        return JsonResponse(eval_comp_data, status=eval_comp_code)
    url = __get_pass_url__(request, 'competence/' + str(eval_comp_data['competence']))
    comp_data, comp_code = __make_json_request__(request, url, fields_only=True)
    if comp_code != 200:
        return JsonResponse(comp_data, comp_code)
    eval_comp_data['competence'] = comp_data['code']
    return JsonResponse(eval_comp_data, safe=False)


def all_competence(request):
    url = __get_pass_url__(request, 'all_competence')
    comps_data, comps_code = __make_json_request__(request, url, fields_only=False)
    result = []
    if comps_code != 200:
        return JsonResponse(comps_data, status=comps_code)
    for c in comps_data:
        pk = c['pk']
        fields = c['fields']
        infos = {'id': pk, 'code': fields['code']}
        result.append(infos)
    return JsonResponse(result, safe=False)


def get_comp_details(request, pk):
    ues_suivies = __get_suivre_ue__(request)
    student_eval_comp_list = set()
    for ue in ues_suivies:
        student_eval_comp_list = student_eval_comp_list.union(set(ue['competences']))
    url = __get_pass_url__(request, 'eval_comp_for_comp/' + str(pk))
    all_evals_data, all_evals_code = __make_json_request__(request, url, fields_only=False)
    comp_eval_comp_list = set()
    for e in all_evals_data:
        comp_eval_comp_list.add(e['pk'])
    eval_comp = student_eval_comp_list & comp_eval_comp_list

    all_ues = __get_suivre_ue__(request)
    ue_for_this_comp = []
    for ue in all_ues:
        if (set(ue['competences']) & eval_comp) != set():
            ue_for_this_comp.append((eval_comp, ue['ue'], ue['periode']))
    ues_details = []
    for eval_comp, ue_id, p in ue_for_this_comp:
        eval_comp_id = eval_comp.pop()
        url = __get_pass_url__(request, 'eval_competence/' + str(eval_comp_id))
        eval_comp_data, eval_comp_code = __make_json_request__(request, url, fields_only=True)
        if eval_comp_code == 200:
            url = __get_pass_url__(request, 'periode/' + str(p))
            periode_data, _ = __make_json_request__(request, url, fields_only=True)
            url = __get_pass_url__(request, 'ue/' + str(ue_id))
            ue_data, _ = __make_json_request__(request, url, fields_only=True)
            del eval_comp_data['competence']
            del eval_comp_data['jetons_tentes']
            eval_comp_data['code_ue'] = ue_data['code']
            eval_comp_data['periode'] = periode_data['code']
            ues_details.append(eval_comp_data)

    url = __get_pass_url__(request, 'competence/' + str(pk))
    comp_data, comp_code = __make_json_request__(request, url, fields_only=True)
    if comp_code != 200:
        return JsonResponse(comp_data, status=comp_code)
    for seuil in range(1, 6):
        del comp_data['seuil' + str(seuil)]
    comp_data['ue_details'] = ues_details
    return JsonResponse(comp_data, safe=False)
