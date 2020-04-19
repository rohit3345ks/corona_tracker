from django.shortcuts import render,redirect
from django.http import HttpResponse
import requests
import json
from dateutil.parser import *

# Create your views here.
def home(request):
    main_url='https://covid19.mathdro.id/api'
    daily_url='https://covid19.mathdro.id/api/daily'
    countrylist_url='https://covid19.mathdro.id/api/countries'
    res=requests.get(main_url).json()
    res2=requests.get(daily_url).json()
    res3=requests.get(countrylist_url).json()['countries']
    reportDate=[]
    confirmed_total=[]
    country_list=[]
    deaths_total=[]
    for i in res2:
        confirmed_total.append(i['confirmed']['total'])
        reportDate.append(i['reportDate'])
        deaths_total.append(i['deaths']['total'])
    date=parse(res['lastUpdate'][:19])  
    for i in res3:
        print(i['name'])
        country_list.append(i['name'])

    context={
        'confirmedCases':res['confirmed']['value'],
        'recoveredCases':res['recovered']['value'],
        'deathCount':res['deaths']['value'],
        'lastUpdate':date,
        'confirmed_total':confirmed_total,
        'deaths_total':deaths_total,
        'reportDate':reportDate,
        'country_list':country_list,
        'bar':False,
    }
    return render(request,'app/index.html',context)
def countryInfo(request):
    if request.method=='POST':
        country=request.POST['c_list']
        print(country)
        country_url=('https://covid19.mathdro.id/api/countries/'+country)
        countrylist_url='https://covid19.mathdro.id/api/countries'
        print(country_url)
        res4=requests.get(country_url).json()
        print(res4)
        res3=requests.get(countrylist_url).json()['countries']
        country_list=[]
        for i in res3:
            country_list.append(i['name'])
        if country=='Nothing':
            return redirect('/')
        else:
            res4=requests.get(country_url).json()
        context={
            'selected_country':country,
            'confirmedCases':res4.get('confirmed').get('value'),
            'recoveredCases':res4.get('recovered').get('value'),
            'deathCount':res4.get('deaths').get('value'),
            'bar':True,
            'lastUpdate':parse(requests.get('https://covid19.mathdro.id/api').json()['lastUpdate'][:19]),
            'country_list':country_list,
        }
        return render(request,'app/index.html',context)
    else:
        return redirect('/')