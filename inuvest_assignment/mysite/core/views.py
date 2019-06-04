from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.shortcuts import render_to_response
import os
import glob
import csv
import xlsxwriter
from django.http import HttpResponse

class Home(TemplateView):
    template_name = 'home.html'

def export_users_csv(request):
    files_path = os.path.join('media','*')
    files = sorted(
    glob.iglob(files_path), key=os.path.getctime, reverse=True)
    file_path = os.path.join(files[0])
    E = 0
    C = 0
    D = 0
    TR14 = 0
    DM_14 = 0
    DM_nv_14  = 0
    temp1 = 0
    temp2 = 0
    temp3 = 0
    temp4 = 0
    counter = 0
    ADX = 0
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Assignment1-Solution1.csv'
    writer = csv.writer(response)
    writer.writerow(['Open', 'High', 'Low', 'Close', 'TR', '+DM 1', '- DM 1','TR 14','+DM 14','-DM 14','+DI 14','-DI 14','DI 14 diff','DI 14 Sum','DX','ADX'])

    with open(file_path, 'r') as f:
        for line in f:
            array = line.split(",")
            if (array[2]!='High' or array[3]!='Low'):
                previous_E = E
                previous_C = C
                previous_D = D
                previous_TR14 = TR14
                previous_DM_14 = DM_14
                previous_DM_nv_14 = DM_nv_14
                previous_ADX = ADX
                C = int(array[2])
                D = int(array[3])
                E = int(array[4])

                TR = (max(C-D, abs(C-previous_E),abs(D- previous_E)))
                DM_1 = (max((C-previous_C),0) if (C - previous_C)>(previous_D - D) else  0)
                DM_nv_1 = (max((previous_D-D),0) if (previous_D - D)>(C - previous_C) else  0)
                counter+=1
                DM_nv_1 = DM_nv_1 if TR!=C else ''
                TR = TR if TR!=C else ''
                DM_1 = DM_1 if DM_1!=C else ''

                if counter > 1 and counter < 16:
                    temp1 = temp1 + TR
                    temp2 = temp2 + DM_1
                    temp3 = temp3 + DM_nv_1
                if counter == 15:
                    TR14 = temp1
                    DM_14 = temp2
                    DM_nv_14 = temp3
                    DI14 = round(100 * (DM_14 / TR14),2)
                    DI_nv_14 = round(100 * (DM_nv_14 / TR14),2)
                    DI14_diff = abs(DI14 - DI_nv_14)
                    DI14_sum = DI14 + DI_nv_14
                    DX = round(100 * (DI14_diff / DI14_sum),2)
                    temp4 = temp4 + DX
                if counter <= 14:
                    TR14 = ''
                    DM_14 = ''
                    DM_nv_14 = ''
                    DI14 = ''
                    DI_nv_14 = ''
                    DI14_diff = ''
                    DI14_sum = ''
                    DX = ''
                    ADX = ''
                if counter >= 16:
                    TR14 = round(previous_TR14 - (previous_TR14/14) + TR,2)
                    DM_14 = round(previous_DM_14 - (previous_DM_14/14) + DM_1,2)
                    DM_nv_14 = round(previous_DM_nv_14 - (previous_DM_nv_14/14) + DM_nv_1,2)
                    DI14 = round(100 * (DM_14 / TR14),2)
                    DI_nv_14 = round(100 * (DM_nv_14 / TR14),2)
                    DI14_diff = abs(DI14 - DI_nv_14)
                    DI14_sum = DI14 + DI_nv_14
                    DX = round(100 * (DI14_diff / DI14_sum),2)
                    temp4 = temp4 + DX
                if counter == 28:
                    ADX = temp4 / 14
                if counter > 28:
                    ADX = round(((previous_ADX*13) + DX) / 14,2)
                array = [array[1],C,D,E,TR,DM_1,DM_nv_1,TR14,DM_14,DM_nv_14,DI14,DI_nv_14,DI14_diff,DI14_sum,DX,ADX]
                writer.writerow(array)
    return response
def upload(request):
    context = {}
    array_DI = []
    array_DI_nv = []
    array_ADX = []
    file_path = ''
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
        file_path = os.path.join('media', uploaded_file.name)
        E = 0
        C = 0
        D = 0
        TR14 = 0
        DM_14 = 0
        DM_nv_14  = 0
        temp1 = 0
        temp2 = 0
        temp3 = 0
        temp4 = 0
        counter = 0
        ADX = 0
        with open(file_path, 'r') as f:
            for line in f:
                array = line.split(",")
                if (array[2]!='High' or array[3]!='Low'):
                    previous_E = E
                    previous_C = C
                    previous_D = D
                    previous_TR14 = TR14
                    previous_DM_14 = DM_14
                    previous_DM_nv_14 = DM_nv_14
                    previous_ADX = ADX
                    C = int(array[2])
                    D = int(array[3])
                    E = int(array[4])

                    TR = (max(C-D, abs(C-previous_E),abs(D- previous_E)))
                    DM_1 = (max((C-previous_C),0) if (C - previous_C)>(previous_D - D) else  0)
                    DM_nv_1 = (max((previous_D-D),0) if (previous_D - D)>(C - previous_C) else  0)
                    counter+=1
                    DM_nv_1 = DM_nv_1 if TR!=C else ''
                    TR = TR if TR!=C else ''
                    DM_1 = DM_1 if DM_1!=C else ''

                    if counter > 1 and counter < 16:
                        temp1 = temp1 + TR
                        temp2 = temp2 + DM_1
                        temp3 = temp3 + DM_nv_1
                    if counter == 15:
                        TR14 = temp1
                        DM_14 = temp2
                        DM_nv_14 = temp3
                        DI14 = round(100 * (DM_14 / TR14),2)
                        DI_nv_14 = round(100 * (DM_nv_14 / TR14),2)
                        array_DI.append(DI14)
                        array_DI_nv.append(DI_nv_14)
                        DI14_diff = abs(DI14 - DI_nv_14)
                        DI14_sum = DI14 + DI_nv_14
                        DX = round(100 * (DI14_diff / DI14_sum),2)
                        temp4 = temp4 + DX
                    if counter <= 14:
                        TR14 = 0
                        DM_14 = 0
                        DM_nv_14 = 0
                        DI14 = 0
                        DI_nv_14 = 0
                        DI14_diff = 0
                        DI14_sum = 0
                        DX = 0
                        ADX = 0
                        array_DI.append(DI14)
                        array_DI_nv.append(DI_nv_14)
                        array_ADX.append(ADX)
                    if counter >= 16:
                        TR14 = round(previous_TR14 - (previous_TR14/14) + TR,2)
                        DM_14 = round(previous_DM_14 - (previous_DM_14/14) + DM_1,2)
                        DM_nv_14 = round(previous_DM_nv_14 - (previous_DM_nv_14/14) + DM_nv_1,2)
                        DI14 = round(100 * (DM_14 / TR14),2)
                        DI_nv_14 = round(100 * (DM_nv_14 / TR14),2)
                        array_DI.append(DI14)
                        array_DI_nv.append(DI_nv_14)
                        DI14_diff = abs(DI14 - DI_nv_14)
                        DI14_sum = DI14 + DI_nv_14
                        DX = round(100 * (DI14_diff / DI14_sum),2)
                        temp4 = temp4 + DX
                    if counter == 28:
                        ADX = temp4 / 14
                        array_ADX.append(ADX)
                    if counter > 28:
                        ADX = round(((previous_ADX*13) + DX) / 14,2)
                        array_ADX.append(ADX)
                    array = [array[1],C,D,E,TR,DM_1,DM_nv_1,TR14,DM_14,DM_nv_14,DI14,DI_nv_14,DI14_diff,DI14_sum,DX,ADX]

    return render( request,'upload.html', {'url':file_path,'array_DI':array_DI,'array_DI_nv':array_DI_nv,'ADX': array_ADX})
