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
    confirmed_total=[0]
    increase_confirmed=[]
    # confirmed_total.append(0)
    country_list=[]
    deaths_total=[0]
    # deaths_total.append(0)
    recovered_total=[0]
    recovered_total.append(res['recovered']['value'])
    increase_recovered=[]
    increase_recovered.append(recovered_total[-1]-recovered_total[-2])
    increase_deaths=[]
    for i in res2:
        confirmed_total.append(i['confirmed']['total'])
        increase_confirmed.append(confirmed_total[-1]-confirmed_total[-2])
        reportDate.append(i['reportDate'])
        deaths_total.append(i['deaths']['total'])
        increase_deaths.append(deaths_total[-1]-deaths_total[-2])
        date=parse(res['lastUpdate'][:19])  
    confirmed_change=increase_confirmed[-1]
    death_change=increase_deaths[-1]
    for i in res3:
        country_list.append(i['name'])

    context={
        'confirmedCases':res['confirmed']['value'],
        'recoveredCases':res['recovered']['value'],
        'deathCount':res['deaths']['value'],
        'lastUpdate':date,
        'confirmed_total':confirmed_total,
        'increase_confirmed':increase_confirmed,
        'increase_deaths':increase_deaths,
        'deaths_total':deaths_total,
        'reportDate':reportDate,
        'confirmed_change':increase_confirmed[-1],  # Showing increase in confirmed cases
        'death_change': increase_deaths[-1],
        'increase_recovered':increase_recovered[-1],  # Showing increase in death cases
        'country_list':country_list,
        'change':5,
        'bar':0,
    }
    return render(request,'app/index.html',context)
def countryInfo(request):
    if request.method=='POST':
        country=request.POST['c_list']
        country_url=('https://covid19.mathdro.id/api/countries/'+country)
        countrylist_url='https://covid19.mathdro.id/api/countries'
        res4=requests.get(country_url).json()
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
            'lastUpdate':parse(requests.get('https://covid19.mathdro.id/api').json()['lastUpdate'][:19]),
            'country_list':country_list,
            'change':0,
            'bar':5,
        }
        return render(request,'app/index.html',context)
    else:
        return redirect('/')