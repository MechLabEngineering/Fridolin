#!/usr/bin/env python
# coding: utf8

from illuminaro import *
import pandas as pd



kinder = {
    # Vorame Name: Gruppe, Frühstück, Mittag, Vesper, Schlaf
    u'Anton Allianz': [1, True, True, False, True],
    u'Antonia Alligator': [1, True, True, True, False],
    u'Berta Benz': [2, True, True, True, False],
    u'Carla Kolumna': [3, True, True, True, False],
    u'Desiree Donnerstag': [4, True, True, True, False],
}

df = pd.DataFrame(index=kinder.keys(), data=kinder.values(), columns=['Gruppe', 'Frühstück', 'Mittag', 'Vesper', 'Schlaf'])
print('Datenframe:')
print df


def kind(name):
    k=Well(
        StaticHeader(name, 3),
        RadioButtons('Status-%s' % name, ['Abgegeben', 'Abgeholt'], label=''),
        CheckboxInput('fruh-%s' % name, False, u'Frühstück'),
        CheckboxInput('mittag-%s' % name, False, u'Mittag'),
        CheckboxInput('vesper-%s' % name, False, u'Vesper'),        
        RadioInputs('schlaf-%s' % name, ['Schlafgruppe', 'Wachgruppe'], ['schlaf', 'wach'], 1)
    )
    return k


def gruppe(gruppennummer, kinderliste):

    g=TabPanel(
        'Gruppe %i' % gruppennummer,
        WellPanel(
            *kinderliste # mit '*' weil Liste entpackt werden muss
        )
    )
    return g


def gruppen(df):

    groupdf = df.groupby('Gruppe')

    gr = []
    for gruppennummer, gruppenmitglieder in groupdf:
        print('Gruppe %i:' % gruppennummer)
        print(gruppenmitglieder)
        print('\n')

        kinderliste = [kind(name) for name in gruppenmitglieder.index.values] # Objektliste
        gr.append(gruppe(gruppennummer, kinderliste))
        
    return gr


gui = SimplePage(
    "Fridolin",
    StaticHeader('Fridolin - KiTa Zeiterfassung :)',1),
    WellPanel(
        TabSet(
            *gruppen(df) # mit '*' weil Liste entpackt werden muss
        )
    ),
    Well(
        MarkupOutput('result', '')
    ),

    TextOutput(id='Impressum', text=u'MechLab Engineering UG (haftungsbeschränkt), Marienstr. 20, 01067 Dresden, Build with Illuminaro and Python, Twitter: @MechLabEng')
)


def server(app, values, outputs, **kwargs):
    if values.Status == 'Abgegeben':
        anz = 1
    else:
        anz = 0

    btu = anz
    outputs.result = '<p>' + str(btu) + '</strong> Kinder anwesend</p>'
    pass


# debug=True enables live code reloading on save
app = IlluminaroApp(gui, None, debug=True)
app.run()
