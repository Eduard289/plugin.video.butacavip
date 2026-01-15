# -*- coding: utf-8 -*-

import sys
import os
import xbmc
from datetime import datetime

from platformcode import config, logger, platformtools, updater
from core.item import Item
from core import channeltools, scrapertools

# Definimos PY3 como True por defecto (Limpieza para Kodi 19/20/21+)
PY3 = True

fanart = os.path.join(config.get_runtime_path(), 'fanart.jpg')

color_list_prefe = config.get_setting('channels_list_prefe_color', default='gold')
color_list_proxies = config.get_setting('channels_list_proxies_color', default='red')
color_list_inactive = config.get_setting('channels_list_inactive_color', default='gray')

color_alert = config.get_setting('notification_alert_color', default='red')
color_infor = config.get_setting('notification_infor_color', default='pink')
color_adver = config.get_setting('notification_adver_color', default='violet')
color_avis = config.get_setting('notification_avis_color', default='yellow')
color_exec = config.get_setting('notification_exec_color', default='cyan')

current_year = int(datetime.today().year)
current_month = int(datetime.today().month)


team = False
if os.path.exists(os.path.join(config.get_runtime_path(), 'modules', 'developergenres.py')): team = True
elif os.path.exists(os.path.join(config.get_runtime_path(), 'modules', 'developertest.py')): team = True
elif os.path.exists(os.path.join(config.get_runtime_path(), 'modules', 'developertools.py')): team = True

config.set_setting('developer_team', team)


avisar = False
kver = str(xbmc.getInfoLabel('System.BuildVersion'))

if not kver:
    kver = 0
    avisar = True
else:
    # Lógica simplificada para versiones modernas
    if kver.startswith('18.'): kver = 18
    elif kver.startswith('19.'): kver = 19
    elif kver.startswith('20.'): kver = 20
    elif kver.startswith('21.'): kver = 21
    elif kver.startswith('22.'): kver = 22
    elif kver.startswith('23.'): kver = 23
    elif kver.startswith('24.'): kver = 24
    else: 
        try:
            kver = int(kver.split('.')[0])
        except:
            kver = 0

kver = int(kver)

if avisar:
    if config.get_setting('developer_mode', default=False):
        if config.get_setting('developer_team'):
            platformtools.dialog_notification(config.__addon_name + ' Media Center', '[COLOR red][B]Versión/Release Desconocida[/COLOR][/B]')


config.set_setting('kver', kver)
config.set_setting('PY3', True)
config.set_setting('ses_pin', False)


con_incidencias = ''
no_accesibles = ''
con_problemas = ''

# Lectura de dominios
try:
    file_path = os.path.join(config.get_runtime_path(), 'dominios.txt')
    with open(file_path, 'r', encoding='utf-8') as f:
        txt_status = f.read()
except Exception:
    txt_status = ''

if txt_status:
    # ~ Incidencias
    bloque = scrapertools.find_single_match(txt_status, 'SITUACION CANALES(.*?)CANALES TEMPORALMENTE DES-ACTIVADOS')
    matches = scrapertools.find_multiple_matches(bloque, "[B](.*?)[/B]")
    for match in matches:
        match = match.strip()
        if '[COLOR moccasin]' in match: 
            con_incidencias += '[B' + match + '/I][/B][/COLOR][CR]'

    # ~ No Accesibles
    bloque = scrapertools.find_single_match(txt_status, 'CANALES PROBABLEMENTE NO ACCESIBLES(.*?)ULTIMOS CAMBIOS DE DOMINIOS')
    matches = scrapertools.find_multiple_matches(bloque, "[B](.*?)[/B]")
    for match in matches:
        match = match.strip()
        if '[COLOR moccasin]' in match: 
            no_accesibles += '[B' + match + '/I][/B][/COLOR][CR]'

    # ~ Con Problemas
    bloque = scrapertools.find_single_match(txt_status, 'CANALES CON PROBLEMAS(.*?)$')
    matches = scrapertools.find_multiple_matches(bloque, "[B](.*?)[/B]")
    for match in matches:
        match = match.strip()
        if '[COLOR moccasin]' in match: 
            con_problemas += '[B' + match + '/I][/B][/COLOR][CR]'


# --- DEFINICIÓN DE CONTEXT MENUS ---

context_desarrollo = []
tit = '[COLOR tan][B]Preferencias Menús[/B][/COLOR]'
context_desarrollo.append({'title': tit, 'channel': 'helper', 'action': 'show_menu_parameters'})
tit = '[COLOR goldenrod][B]Miscelánea[/B][/COLOR]'
context_desarrollo.append({'title': tit, 'channel': 'helper', 'action': 'show_help_miscelanea'})
tit = '[COLOR %s]Ajustes categoría Team[/COLOR]' % color_exec
context_desarrollo.append({'title': tit, 'channel': 'actions', 'action': 'open_settings'})

context_menu = []
tit = '[COLOR tan][B]Preferencias Menús[/B][/COLOR]'
context_menu.append({'title': tit, 'channel': 'helper', 'action': 'show_menu_parameters'})
tit = '[COLOR fuchsia][B]Preferencias Play[/B][/COLOR]'
context_menu.append({'title': tit, 'channel': 'helper', 'action': 'show_play_parameters'})
tit = '[COLOR powderblue][B]Preferencias Buscar[/B][/COLOR]'
context_menu.append({'title': tit, 'channel': 'helper', 'action': 'show_help_parameters_search'})
tit = '[COLOR %s]Ajustes categorías Menú, Play y Buscar[/COLOR]' % color_exec
context_menu.append({'title': tit, 'channel': 'actions', 'action': 'open_settings'})

context_buscar = []
tit = '[COLOR tan][B]Preferencias Menús[/B][/COLOR]'
context_buscar.append({'title': tit, 'channel': 'helper', 'action': 'show_menu_parameters'})
tit = '[COLOR fuchsia][B]Preferencias Play[/B][/COLOR]'
context_buscar.append({'title': tit, 'channel': 'helper', 'action': 'show_play_parameters'})
tit = '[COLOR powderblue][B]Preferencias Buscar[/B][/COLOR]'
context_buscar.append({'title': tit, 'channel': 'helper', 'action': 'show_help_parameters_search'})
tit = '[COLOR darkcyan][B]Preferencias Proxies[/B][/COLOR]'
context_buscar.append({'title': tit, 'channel': 'helper', 'action': 'show_prx_parameters'})
tit = '[COLOR bisque]Gestión Dominios[/COLOR]'
context_buscar.append({'title': tit, 'channel': 'helper', 'action': 'show_help_domains'})
tit = '[COLOR mediumaquamarine][B]Últimos Cambios Dominios[/B][/COLOR]'
context_buscar.append({'title': tit, 'channel': 'actions', 'action': 'show_latest_domains'})
tit = '[COLOR darkorange][B]Quitar Dominios Memorizados[/B][/COLOR]'
context_buscar.append({'title': tit, 'channel': 'actions', 'action': 'manto_domains'})
tit = '[COLOR gold][B]Qué Canales No Intervienen[/B][/COLOR]'
context_buscar.append({'title': tit, 'channel': 'helper', 'action': 'channels_no_searchables'})
tit = '[COLOR gray][B]Qué Canales están Desactivados[/B][/COLOR]'
context_buscar.append({'title': tit, 'channel': 'filters', 'action': 'no_actives'})
tit = '[COLOR yellow][B]Búsquedas Solo en ...[/B][/COLOR]'
context_buscar.append({'title': tit, 'channel': 'submnuctext', 'action': '_channels_included'})

if config.get_setting('search_included_all', default=''):
    tit = '[COLOR indianred][B]Quitar Búsquedas Solo en ...[/B][/COLOR]'
    context_buscar.append({'title': tit, 'channel': 'submnuctext', 'action': '_channels_included_del'})

tit = '[COLOR greenyellow][B]Excluir Canales[/B][/COLOR]'
context_buscar.append({'title': tit, 'channel': 'submnuctext', 'action': '_channels_excluded'})

if config.get_setting('search_excludes_all', default=''):
    tit = '[COLOR violet][B]Quitar Canales Excluidos[/B][/COLOR]'
    context_buscar.append({'title': tit, 'channel': 'submnuctext', 'action': '_channels_excluded_del'})

if config.get_setting('search_excludes_movies', default=''):
    tit = '[B][COLOR deepskyblue]Películas [COLOR violet]Quitar Canales Excluidos [/B][/COLOR]'
    context_buscar.append({'title': tit, 'channel': 'submnuctext', 'action': '_channels_excluded_del_movies'})

if config.get_setting('search_excludes_tvshows', default=''):
    tit = '[B][COLOR hotpink]Series [COLOR violet]Quitar Canales Excluidos [/B][/COLOR]'
    context_buscar.append({'title': tit, 'channel': 'submnuctext', 'action': '_channels_excluded_del_tvshows'})

if config.get_setting('search_excludes_documentaries', default=''):
    tit = '[B][COLOR cyan]Documentales [COLOR violet]Quitar Canales Excluidos [/B][/COLOR]'
    context_buscar.append({'title': tit, 'channel': 'submnuctext', 'action': '_channels_excluded_del_documentaries'})

if config.get_setting('search_excludes_torrents', default=''):
    tit = '[B][COLOR blue]Torrents [COLOR violet]Quitar Canales Excluidos [/B][/COLOR]'
    context_buscar.append({'title': tit, 'channel': 'submnuctext', 'action': '_channels_excluded_del_torrents'})

if config.get_setting('search_excludes_mixed', default=''):
    tit = '[B][COLOR teal]Películas y/ó Series [COLOR violet]Quitar Canales Excluidos [/B][/COLOR]'
    context_buscar.append({'title': tit, 'channel': 'submnuctext', 'action': '_channels_excluded_del_mixed'})

tit = '[COLOR powderblue][B]Global Configurar Proxies[/B][/COLOR]'
context_buscar.append({'title': tit, 'channel': 'proxysearch', 'action': 'proxysearch_all'})

if config.get_setting('proxysearch_excludes', default=''):
    tit = '[COLOR %s]Anular canales excluidos de Proxies[/COLOR]' % color_adver
    context_buscar.append({'title': tit, 'channel': 'proxysearch', 'action': 'channels_proxysearch_del'})

tit = '[COLOR %s]Información Proxies[/COLOR]' % color_infor
context_buscar.append({'title': tit, 'channel': 'helper', 'action': 'show_help_proxies'})
tit = '[COLOR %s][B]Quitar Todos los Proxies[/B][/COLOR]' % color_list_proxies
context_buscar.append({'title': tit, 'channel': 'actions', 'action': 'manto_proxies'})
tit = '[COLOR %s][B]Información Búsquedas[/B][/COLOR]' % color_infor
context_buscar.append({'title': tit, 'channel': 'helper', 'action': 'show_help_search'})
tit = '[COLOR %s]Ajustes categorías Canales, Dominios, Play, Proxies y Buscar[/COLOR]' % color_exec
context_buscar.append({'title': tit, 'channel': 'actions', 'action': 'open_settings'})

context_generos = []
tit = '[COLOR tan][B]Preferencias Menús[/B][/COLOR]'
context_generos.append({'title': tit, 'channel': 'helper', 'action': 'show_menu_parameters'})
tit = '[COLOR mediumaquamarine][B]Últimos Cambios Dominios[/B][/COLOR]'
context_generos.append({'title': tit, 'channel': 'actions', 'action': 'show_latest_domains'})
tit = '[COLOR powderblue][B]Global Configurar Proxies[/B][/COLOR]'
context_generos.append({'title': tit, 'channel': 'proxysearch', 'action': 'proxysearch_all'})

if config.get_setting('proxysearch_excludes', default=''):
    tit = '[COLOR %s]Anular canales excluidos de Proxies[/COLOR]' % color_adver
    context_generos.append({'title': tit, 'channel': 'proxysearch', 'action': 'channels_proxysearch_del'})

tit = '[COLOR %s]Información Proxies[/COLOR]' % color_infor
context_generos.append({'title': tit, 'channel': 'helper', 'action': 'show_help_proxies'})
tit = '[COLOR %s][B]Quitar Todos los Proxies[/B][/COLOR]' % color_list_proxies
context_generos.append({'title': tit, 'channel': 'actions', 'action': 'manto_proxies'})
tit = '[COLOR %s]Ajustes categorías Menú, Canales, Dominios y Proxies[/COLOR]' % color_exec
context_generos.append({'title': tit, 'channel': 'actions', 'action': 'open_settings'})

context_proxy_channels = []
tit = '[COLOR tan][B]Preferencias Menús[/B][/COLOR]'
context_proxy_channels.append({'title': tit, 'channel': 'helper', 'action': 'show_menu_parameters'})
tit = '[COLOR mediumaquamarine][B]Últimos Cambios Dominios[/B][/COLOR]'
context_proxy_channels.append({'title': tit, 'channel': 'actions', 'action': 'show_latest_domains'})
tit = '[COLOR powderblue][B]Global Configurar Proxies[/B][/COLOR]'
context_proxy_channels.append({'title': tit, 'channel': 'proxysearch', 'action': 'proxysearch_all'})

if config.get_setting('proxysearch_excludes', default=''):
    tit = '[COLOR %s]Anular canales excluidos de Proxies[/COLOR]' % color_adver
    context_proxy_channels.append({'title': tit, 'channel': 'proxysearch', 'action': 'channels_proxysearch_del'})

tit = '[COLOR %s]Información Proxies[/COLOR]' % color_avis
context_proxy_channels.append({'title': tit, 'channel': 'helper', 'action': 'show_help_proxies'})
tit = '[COLOR %s][B]Quitar Todos los Proxies[/B][/COLOR]' % color_list_proxies
context_proxy_channels.append({'title': tit, 'channel': 'actions', 'action': 'manto_proxies'})
tit = '[COLOR %s]Ajustes categorías Menú, Canales, Dominios y Proxies[/COLOR]' % color_exec
context_proxy_channels.append({'title': tit, 'channel': 'actions', 'action': 'open_settings'})

context_cfg_search = []
tit = '[COLOR tan][B]Preferencias Menús[/B][/COLOR]'
context_cfg_search.append({'title': tit, 'channel': 'helper', 'action': 'show_menu_parameters'})
tit = '[COLOR %s]Ajustes categoría Menú[/COLOR]' % color_exec
context_cfg_search.append({'title': tit, 'channel': 'actions', 'action': 'open_settings'})

context_torrents = []
tit = '[COLOR tan][B]Preferencias Canales[/B][/COLOR]'
context_torrents.append({'title': tit, 'channel': 'helper', 'action': 'show_channels_parameters'})
tit = '[COLOR mediumaquamarine][B]Últimos Cambios Dominios[/B][/COLOR]'
context_torrents.append({'title': tit, 'channel': 'actions', 'action': 'show_latest_domains'})

if config.get_setting('cliente_torrent') == 'Seleccionar' or config.get_setting('cliente_torrent') == 'Ninguno':
    tit = '[COLOR %s][B]Información Motores Torrent[/B][/COLOR]' % color_infor
    context_torrents.append({'title': tit, 'channel': 'helper', 'action': 'show_help_torrents'})

tit = '[COLOR %s][B]Motores torrents instalados[/B][/COLOR]' % color_avis
context_torrents.append({'title': tit, 'channel': 'helper', 'action': 'show_clients_torrent'})
tit = '[COLOR powderblue][B]Global Configurar Proxies[/B][/COLOR]'
context_torrents.append({'title': tit, 'channel': 'proxysearch', 'action': 'proxysearch_all'})

if config.get_setting('proxysearch_excludes', default=''):
    tit = '[COLOR %s]Anular canales excluidos de Proxies[/COLOR]' % color_adver
    context_torrents.append({'title': tit, 'channel': 'proxysearch', 'action': 'channels_proxysearch_del'})

tit = '[COLOR %s]Información Proxies[/COLOR]' % color_avis
context_torrents.append({'title': tit, 'channel': 'helper', 'action': 'show_help_proxies'})
tit = '[COLOR %s][B]Quitar Todos los Proxies[/B][/COLOR]' % color_list_proxies
context_torrents.append({'title': tit, 'channel': 'actions', 'action': 'manto_proxies'})
tit = '[COLOR %s]Ajustes categorías Canales, Dominios, Proxies y Torrents[/COLOR]' % color_exec
context_torrents.append({'title': tit, 'channel': 'actions', 'action': 'open_settings'})

context_parental = []
tit = '[COLOR tan][B]Preferencias Canales[/B][/COLOR]'
context_parental.append({'title': tit, 'channel': 'helper', 'action': 'show_channels_parameters'})
tit = '[COLOR mediumaquamarine][B]Últimos Cambios Dominios[/B][/COLOR]'
context_parental.append({'title': tit, 'channel': 'actions', 'action': 'show_latest_domains'})

if config.get_setting('adults_password'):
    tit = '[COLOR %s][B]Eliminar Pin Parental[/B][/COLOR]' % color_adver
    context_parental.append({'title': tit, 'channel': 'actions', 'action': 'adults_password_del'})
else:
    tit = '[COLOR %s][B]Información Parental[/B][/COLOR]' % color_infor
    context_parental.append({'title': tit, 'channel': 'helper', 'action': 'show_help_adults'})
    tit = '[COLOR %s][B]Establecer Pin Parental[/B][/COLOR]' % color_avis
    context_parental.append({'title': tit, 'channel': 'actions', 'action': 'adults_password'})

tit = '[COLOR powderblue][B]Global Configurar Proxies[/B][/COLOR]'
context_parental.append({'title': tit, 'channel': 'proxysearch', 'action': 'proxysearch_all'})

if config.get_setting('proxysearch_excludes', default=''):
    tit = '[COLOR %s]Anular canales excluidos de Proxies[/COLOR]' % color_adver
    context_parental.append({'title': tit, 'channel': 'proxysearch', 'action': 'channels_proxysearch_del'})

tit = '[COLOR %s]Información Proxies[/COLOR]' % color_avis
context_parental.append({'title': tit, 'channel': 'helper', 'action': 'show_help_proxies'})
tit = '[COLOR %s][B]Quitar Todos los Proxies[/B][/COLOR]' % color_list_proxies
context_parental.append({'title': tit, 'channel': 'actions', 'action': 'manto_proxies'})
tit = '[COLOR %s]Ajustes categorías Canales, Parental, Dominios y Proxies[/COLOR]' % color_exec
context_parental.append({'title': tit, 'channel': 'actions', 'action': 'open_settings'})

context_adultos = []
tit = '[COLOR tan][B]Preferencias Canales[/B][/COLOR]'
context_adultos.append({'title': tit, 'channel': 'helper', 'action': 'show_channels_parameters'})
tit = '[COLOR mediumaquamarine][B]Últimos Cambios Dominios[/B][/COLOR]'
context_adultos.append({'title': tit, 'channel': 'actions', 'action': 'show_latest_domains'})

if config.get_setting('adults_password'):
    tit = '[COLOR %s][B]Eliminar Pin Parental[/B][/COLOR]' % color_adver
    context_adultos.append({'title': tit, 'channel': 'actions', 'action': 'adults_password_del'})
else:
    tit = '[COLOR %s][B]Información Parental[/B][/COLOR]' % color_infor
    context_adultos.append({'title': tit, 'channel': 'helper', 'action': 'show_help_adults'})
    tit = '[COLOR %s][B]Establecer Pin Parental[/B][/COLOR]' % color_avis
    context_adultos.append({'title': tit, 'channel': 'actions', 'action': 'adults_password'})

tit = '[COLOR %s]Ajustes categorías Canales, Parental y Dominios[/COLOR]' % color_exec
context_adultos.append({'title': tit, 'channel': 'actions', 'action': 'open_settings'})

context_desactivados = []
tit = '[COLOR tan][B]Preferencias Menús[/B][/COLOR]'
context_desactivados.append({'title': tit, 'channel': 'helper', 'action': 'show_menu_parameters'})
tit = '[COLOR mediumaquamarine][B]Últimos Cambios Dominios[/B][/COLOR]'
context_desactivados.append({'title': tit, 'channel': 'actions', 'action': 'show_latest_domains'})
tit = '[COLOR %s]Ajustes categorías Menú, Dominios y Canales[/COLOR]' % color_exec
context_desactivados.append({'title': tit, 'channel': 'actions', 'action': 'open_settings'})

context_preferidos = []
tit = '[COLOR tan][B]Preferencias Menús[/B][/COLOR]'
context_preferidos.append({'title': tit, 'channel': 'helper', 'action': 'show_menu_parameters'})
tit = '[COLOR mediumaquamarine][B]Últimos Cambios Dominios[/B][/COLOR]'
context_preferidos.append({'title': tit, 'channel': 'actions', 'action': 'show_latest_domains'})
tit = '[COLOR %s][B]Información Preferidos[/B][/COLOR]' % color_infor
context_preferidos.append({'title': tit, 'channel': 'helper', 'action': 'show_help_tracking'})
tit = '[COLOR %s][B]Comprobar Nuevos Episodios[/B][/COLOR]' % color_adver
context_preferidos.append({'title': tit, 'channel': 'actions', 'action': 'comprobar_nuevos_episodios'})
tit = '[COLOR %s][B]Eliminar Todos los Preferidos[/B][/COLOR]' % color_alert
context_preferidos.append({'title': tit, 'channel': 'actions', 'action': 'manto_tracking_dbs'})
tit = '[COLOR %s]Ajustes categorías Menú, Dominios y Preferidos[/COLOR]' % color_exec
context_preferidos.append({'title': tit, 'channel': 'actions', 'action': 'open_settings'})

context_descargas = []
tit = '[COLOR tan][B]Preferencias Menús[/B][/COLOR]'
context_descargas.append({'title': tit, 'channel': 'helper', 'action': 'show_menu_parameters'})
tit = '[COLOR mediumaquamarine][B]Últimos Cambios Dominios[/B][/COLOR]'
context_descargas.append({'title': tit, 'channel': 'actions', 'action': 'show_latest_domains'})
tit = '[COLOR %s][B]Información Descargas[/B][/COLOR]' % color_adver
context_descargas.append({'title': tit, 'channel': 'helper', 'action': 'show_help_descargas'})
tit = '[COLOR %s][B]Ubicación Descargas[/B][/COLOR]' % color_infor
context_descargas.append({'title': tit, 'channel': 'downloads', 'action': 'show_folder_downloads'})
tit = '[COLOR %s][B]Eliminar Todas las Descargas[/B][/COLOR]' % color_alert
context_descargas.append({'title': tit, 'channel': 'actions', 'action': 'manto_folder_downloads'})
tit = '[COLOR %s]Ajustes categoría Menú, Dominios y Descargas[/COLOR]' % color_exec
context_descargas.append({'title': tit, 'channel': 'actions', 'action': 'open_settings'})

context_config = []
tit = '[COLOR tan][B]Preferencias Canales[/B][/COLOR]'
context_config.append({'title': tit, 'channel': 'helper', 'action': 'show_channels_parameters'})
tit = '[COLOR bisque]Gestión Dominios[/COLOR]'
context_config.append({'title': tit, 'channel': 'helper', 'action': 'show_help_domains'})
tit = '[COLOR %s][B]Últimos Cambios Dominios[/B][/COLOR]' % color_exec
context_config.append({'title': tit, 'channel': 'actions', 'action': 'show_latest_domains'})
tit = '[COLOR darkorange][B]Quitar Dominios Memorizados[/B][/COLOR]'
context_config.append({'title': tit, 'channel': 'actions', 'action': 'manto_domains'})
tit = '[COLOR green][B]Información Plataforma[/B][/COLOR]'
context_config.append({'title': tit, 'channel': 'helper', 'action': 'show_plataforma'})
tit = '[COLOR %s][B]Quitar Todos los Proxies[/B][/COLOR]' % color_alert
context_config.append({'title': tit, 'channel': 'actions', 'action': 'manto_proxies'})
tit = '[COLOR olive][B]Limpiezas[/B][/COLOR]'
context_config.append({'title': tit, 'channel': 'actions', 'action': 'manto_limpiezas'})
tit = '[COLOR orange][B]Borrar Carpeta Caché[/B][/COLOR]'
context_config.append({'title': tit, 'channel': 'actions', 'action': 'manto_folder_cache'})
tit = '[COLOR %s][B]Sus Ajustes Personalizados[/B][/COLOR]' % color_avis
context_config.append({'title': tit, 'channel': 'helper', 'action': 'show_sets'})
tit = '[COLOR %s]Cookies Actuales[/COLOR]' % color_infor
context_config.append({'title': tit, 'channel': 'helper', 'action': 'show_cook'})
tit = '[COLOR %s][B]Eliminar Cookies[/B][/COLOR]' % color_infor
context_config.append({'title': tit, 'channel': 'actions', 'action': 'manto_cookies'})
tit = '[COLOR %s]Sus Advanced Settings[/COLOR]' % color_adver
context_config.append({'title': tit, 'channel': 'helper', 'action': 'show_advs'})
tit = '[COLOR fuchsia][B]Eliminar Advanced Settings[/B][/COLOR]'
context_config.append({'title': tit, 'channel': 'actions', 'action': 'manto_advs'})
tit = '[COLOR mediumaquamarine][B]Restablecer Parámetros Internos[/B][/COLOR]'
context_config.append({'title': tit, 'channel': 'actions', 'action': 'manto_params'})

context_usual = []
tit = '[COLOR tan][B]Preferencias Canales[/B][/COLOR]'
context_usual.append({'title': tit, 'channel': 'helper', 'action': 'show_channels_parameters'})
tit = '[COLOR mediumaquamarine][B]Últimos Cambios Dominios[/B][/COLOR]'
context_usual.append({'title': tit, 'channel': 'actions', 'action': 'show_latest_domains'})
tit = '[COLOR powderblue][B]Global Configurar Proxies[/B][/COLOR]'
context_usual.append({'title': tit, 'channel': 'proxysearch', 'action': 'proxysearch_all'})

if config.get_setting('proxysearch_excludes', default=''):
    tit = '[COLOR %s]Anular canales excluidos de Proxies[/COLOR]' % color_adver
    context_usual.append({'title': tit, 'channel': 'proxysearch', 'action': 'channels_proxysearch_del'})

tit = '[COLOR %s]Información Proxies[/COLOR]' % color_avis
context_usual.append({'title': tit, 'channel': 'helper', 'action': 'show_help_proxies'})
tit = '[COLOR %s][B]Quitar Todos los Proxies[/B][/COLOR]' % color_list_proxies
context_usual.append({'title': tit, 'channel': 'actions', 'action': 'manto_proxies'})
tit = '[COLOR %s]Ajustes categorías Canales, Dominios y Proxies[/COLOR]' % color_exec
context_usual.append({'title': tit, 'channel': 'actions', 'action': 'open_settings'})


# Asegúrate de tener estos imports al inicio del archivo mainmenu.py
# Si no los tienes, agrégalos arriba del todo junto a los otros imports:
import json
import time

def mainlist(item):
    logger.info()
    itemlist = []
    item.category = config.__addon_name

    # --- FUNCIÓN AUXILIAR: CACHÉ DE ESTRENOS (Optimización) ---
    def get_cached_estrenos():
        cache_file = os.path.join(config.get_data_path(), 'estrenos_cache.json')
        cache_time = 4 * 60 * 60  # 4 horas (en segundos)
        data = None
        
        # 1. Intentamos leer la caché
        if os.path.exists(cache_file):
            try:
                if (time.time() - os.path.getmtime(cache_file)) < cache_time:
                    with open(cache_file, 'r') as f:
                        data = json.load(f)
            except: pass

        # 2. Si no hay caché válida, descargamos (solo ocurrirá cada 4h)
        if not data:
            try:
                try: from channels import filmaffinitylists
                except ImportError: import filmaffinitylists
                
                item_scrape = Item(channel='filmaffinitylists', action='list_all', url='https://www.filmaffinity.com/es/cat_new_th_es.html', search_type='movie')
                lista_items = filmaffinitylists.list_all(item_scrape)
                
                data = []
                count = 0
                for p in lista_items:
                    if count >= 3: break
                    data.append({
                        'title': p.title,
                        'url': p.url,
                        'thumbnail': p.thumbnail,
                        'plot': p.plot
                    })
                    count += 1
                
                with open(cache_file, 'w') as f:
                    json.dump(data, f)
            except Exception as e:
                logger.error("Error generando caché estrenos: " + str(e))
                return []

        # 3. Reconstruimos los Items
        result_list = []
        if data:
            for d in data:
                # Reconstrucción manual para asegurar compatibilidad
                it = Item() 
                it.channel = 'filmaffinitylists'
                it.action = 'find_videos'
                it.title = d['title']
                it.url = d['url']
                it.thumbnail = d['thumbnail']
                it.plot = d.get('plot', '')
                result_list.append(it)
                
        return result_list

    # --- SEPARADOR VISUAL ---

    def add_separator():
        # Usamos la ruta de 'themes/default' que es la estándar para iconos del sistema
        ruta_imagen = os.path.join(
            config.get_runtime_path(), 
            'resources', 'media', 'themes', 'default', 'separator.png'
        )
        
        itemlist.append(item.clone(
            action='', 
            title='[COLOR dimgray]──────────────────────────────────────────[/COLOR]', 
            thumbnail=ruta_imagen, 
            plot='', 
            folder=False
        ))

    # --- MODO DESARROLLADOR ---
    if config.get_setting('developer_mode', default=False):
        titulo = '[B]Desarrollo[/B]'
        if not config.get_setting('developer_team'): titulo = '[B]Falso Desarrollo[/B]'
        itemlist.append(item.clone( channel='submnuteam', action='submnu_team', title = titulo, context=context_desarrollo, thumbnail=config.get_thumb('team'), fanart=fanart ))

    # =========================================================================
    # BLOQUE 1: ESTRENOS (Caché ultrarrápida)
    # =========================================================================
    
    lista_estrenos = get_cached_estrenos()
    if lista_estrenos:
        for peli in lista_estrenos:
            peli.title = '[B]Estreno:[/B] ' + peli.title
            itemlist.append(item.clone(
                channel='filmaffinitylists',
                action='find_videos',
                title=peli.title,
                url=peli.url,
                thumbnail=peli.thumbnail,
                plot=peli.plot,
                fanart=fanart,
                contentTitle=peli.title.replace('[B]Estreno:[/B] ', '')
            ))

    add_separator()

    # =========================================================================
    # BLOQUE 2: ZONA TMDB
    # =========================================================================
    
    itemlist.append(item.clone(
        channel='tmdblists', action='listado', title='[B]Cartelera TMDB[/B] (Ver todas)',
        extra='now_playing', search_type='movie',
        thumbnail=config.get_thumb('tmdb'), fanart=fanart,
        plot='Los últimos estrenos de cine actualizados desde The Movie Database'
    ))

    itemlist.append(item.clone( 
        channel='tmdblists', action='mainlist', title='[B]Listas TMDB[/B] (Populares, Valoradas...)', 
        plot='Explora listas populares, mejor valoradas, por recaudación, etc.',
        thumbnail=config.get_thumb('tmdb'), fanart=fanart
    ))

    # =========================================================================
    # BLOQUE 3: ZONA FILMAFFINITY
    # =========================================================================

    itemlist.append(item.clone(
        channel='filmaffinitylists', action='list_all', url='https://www.filmaffinity.com/es/cat_new_th_es.html',
        title='[B]Cartelera Filmaffinity[/B] (Ver todas)', search_type='movie',
        thumbnail=config.get_thumb('filmaffinity'), fanart=fanart,
        plot='La cartelera de cines España según Filmaffinity'
    ))

    itemlist.append(item.clone( 
        channel='filmaffinitylists', action='mainlist', title='[B]Listas Filmaffinity[/B] (Temas, Premios...)', 
        plot='Explora listas por temas, plataformas, premios Oscars, Goyas...',
        thumbnail=config.get_thumb('filmaffinity'), fanart=fanart
    ))

    add_separator()

    # =========================================================================
    # BLOQUE 4: HERRAMIENTAS
    # =========================================================================

    itemlist.append(Item( channel='search', action='mainlist', title='[B]Buscar[/B]', context=context_buscar, thumbnail=config.get_thumb('search'), mnupral = 'main', fanart=fanart ))

    if config.get_setting('sub_mnu_news', default=True):
        itemlist.append(item.clone( channel='submnuctext', action='submnu_news', title='[B]Novedades[/B]', context=context_cfg_search, extra = 'all',thumbnail=config.get_thumb('novedades'), fanart=fanart, mnupral = 'main' ))

    if config.get_setting('sub_mnu_special', default=True):
        itemlist.append(item.clone( channel='submnuctext', action='submnu_special', title='[B]Especiales[/B]', context=context_cfg_search, extra='all', thumbnail=config.get_thumb('heart'), fanart=fanart, mnupral = 'main' ))

    if config.get_setting('sub_mnu_favoritos', default=False):
        itemlist.append(item.clone( channel='favoritos', action='mainlist', title='[B]Mis Favoritos[/B]', context=context_cfg_search, thumbnail=config.get_thumb('star'), fanart=fanart ))

    if not config.get_setting('mnu_simple', default=False):
        if config.get_setting('mnu_desargas', default=True) and config.get_setting('ord_descargas', default=False):
            itemlist.append(item.clone( channel='downloads', action='mainlist', title='[B]Descargas[/B]', context=context_descargas, thumbnail=config.get_thumb('downloads'), fanart=fanart ))

    add_separator()

    # =========================================================================
    # BLOQUE 5: CATEGORÍAS
    # =========================================================================

    mnu_type = '[B]Explorar por Categorías[/B]'
    itemlist.append(item.clone( action='', title=mnu_type, context=context_menu, thumbnail=config.get_thumb('stack'), fanart=fanart, text_color='white' ))

    if config.get_setting('channels_link_main', default=True):
        itemlist.append(item.clone( action='channels', extra='all', title='Todos los Canales', context=context_usual, detallar = True, thumbnail=config.get_thumb('stack'), fanart=fanart ))

    if config.get_setting('mnu_pelis', default=True):
        itemlist.append(item.clone( action='channels', extra='movies', title='Películas', context=context_usual, thumbnail=config.get_thumb('movie'), fanart=fanart ))

    if config.get_setting('mnu_series', default=True):
        itemlist.append(item.clone( action='channels', extra='tvshows', title='Series', context=context_usual, thumbnail=config.get_thumb('tvshow'), fanart=fanart ))

    if config.get_setting('channels_link_pyse', default=False):
       itemlist.append(item.clone( action='channels', extra='mixed', title='Películas y Series', context=context_usual, no_docs = True, detallar = True, thumbnail=config.get_thumb('booklet'), fanart=fanart ))

    if config.get_setting('mnu_generos', default=True):
        itemlist.append(item.clone( channel='submnuctext', action='submnu_genres', title= 'Géneros', context=context_generos, thumbnail=config.get_thumb('genres'), fanart=fanart, mnupral = 'main' ))

    if config.get_setting('mnu_torrents', default=True):
        itemlist.append(item.clone( action='channels', extra='torrents', title='Torrents', context=context_torrents, thumbnail=config.get_thumb('torrents'), fanart=fanart ))

    if config.get_setting('mnu_animes', default=True):
        itemlist.append(item.clone( action='channels', extra='anime', title='Animes', context=context_parental, thumbnail=config.get_thumb('anime'), fanart=fanart ))

    if config.get_setting('mnu_proxies', default=False):
        itemlist.append(item.clone( action='channels', extra='proxies', title='Proxies', context=context_proxy_channels, thumbnail=config.get_thumb('stack'), fanart=fanart ))

    add_separator()

    # =========================================================================
    # BLOQUE 6: SISTEMA
    # =========================================================================

    try: last_ver = updater.check_addon_version()
    except: last_ver = None
    if last_ver is None: last_ver = ''
    elif not last_ver: last_ver = ' [COLOR violet](Update)[/COLOR]'
    else: last_ver = ''

    title = '[B]Sistema y Ayuda[/B] %s' % last_ver
    # Icono ajustado a settings o help según prefieras
    itemlist.append(item.clone( action='ayuda', title=title, thumbnail=config.get_thumb('settings'), fanart=fanart ))

    return itemlist


def channels(item):
    logger.info()
    itemlist = []

    # Variables declaradas para posibles usos futuros, aunque las miniaturas se manejan dinámicamente arriba
    thumb_filmaffinity = os.path.join(config.get_runtime_path(), 'resources', 'media', 'channels', 'thumb', 'filmaffinity.jpg')
    thumb_tmdb = os.path.join(config.get_runtime_path(), 'resources', 'media', 'channels', 'thumb', 'tmdb.jpg')

    if item.extra == 'movies':
        if config.get_setting('mnu_search_proxy_channels', default=False):
            itemlist.append(item.clone( channel='submnuctext', action='submnu_search', title='[B]Buscar Nuevos Proxies[/B]', context=context_proxy_channels, only_options_proxies = True, thumbnail=config.get_thumb('flame'), fanart=fanart, text_color='red' ))

        if config.get_setting('sub_mnu_favoritos', default=False):
            itemlist.append(item.clone( channel='favoritos', action='mainlist', title='[B]Favoritos[/B]', context=context_cfg_search, thumbnail=config.get_thumb('star'), fanart=fanart, text_color='plum' ))

        if config.get_setting('sub_mnu_news', default=True):
            itemlist.append(item.clone( channel='submnuctext', action='submnu_news', title='[B]Novedades[/B]', context=context_cfg_search, extra = 'movies', thumbnail=config.get_thumb('novedades'), fanart=fanart, text_color='darksalmon' ))

        if config.get_setting('sub_mnu_special', default=True):
            itemlist.append(item.clone( channel='submnuctext', action='submnu_special', title='[B]Especiales[/B]', context=context_cfg_search, extra='movies', thumbnail=config.get_thumb('heart'), fanart=fanart, text_color='pink' ))

        itemlist.append(item.clone( channel='submnuctext', action='submnu_channels', title='[B]Buscar[/B]', context=context_buscar, extra = 'movies', thumbnail=config.get_thumb('search'), fanart=fanart, text_color='yellow' ))

        if config.get_setting('mnu_grupos', default=True):
            itemlist.append(item.clone( channel='groups', action='mainlist', extra='groups', title='[B]Grupos[/B]', context=context_cfg_search, thumbnail=config.get_thumb('bookshelf'), fanart=fanart, text_color='magenta' ))

        if config.get_setting('mnu_generos', default=True):
           itemlist.append(item.clone( channel='generos', action='mainlist', title= '[B]Géneros[/B]', tip_sel = 'movie', context=context_generos, thumbnail=config.get_thumb('genres'), fanart=fanart, text_color='thistle' ))

        item.category = 'Canales con Películas'
        itemlist.append(item.clone( action='', title='[B]- [I]Películas:[/I][/B]', context=context_usual, plot=item.category, thumbnail=config.get_thumb('movie'), fanart=fanart, text_color='deepskyblue' ))

        accion = 'mainlist_pelis'
        filtros = {'categories': 'movie'}

    elif item.extra == 'tvshows':
        if config.get_setting('mnu_search_proxy_channels', default=False):
            itemlist.append(item.clone( channel='submnuctext', action='submnu_search', title='[B]Buscar Nuevos Proxies[/B]', context=context_proxy_channels, only_options_proxies = True, thumbnail=config.get_thumb('flame'), fanart=fanart, text_color='red' ))

        if config.get_setting('sub_mnu_favoritos', default=False):
            itemlist.append(item.clone( channel='favoritos', action='mainlist', title='[B]Favoritos[/B]', context=context_cfg_search, thumbnail=config.get_thumb('star'), fanart=fanart, text_color='plum' ))

        if config.get_setting('sub_mnu_news', default=True):
            itemlist.append(item.clone( channel='submnuctext', action='submnu_news', title='[B]Novedades[/B]', context=context_cfg_search, extra = 'tvshows', thumbnail=config.get_thumb('novedades'), fanart=fanart, text_color='darksalmon' ))

        if config.get_setting('sub_mnu_special', default=True):
            itemlist.append(item.clone( channel='submnuctext', action='submnu_special', title='[B]Especiales[/B]', context=context_cfg_search, extra='tvshows', thumbnail=config.get_thumb('heart'), fanart=fanart, text_color='pink' ))

        itemlist.append(item.clone( channel='submnuctext', action='submnu_channels', title='[B]Buscar[/B]', context=context_buscar, extra = 'tvshows', thumbnail=config.get_thumb('search'), fanart=fanart, text_color='yellow' ))

        if config.get_setting('mnu_grupos', default=True):
           itemlist.append(item.clone( channel='generos', action='mainlist', title= '[B]Géneros[/B]', tip_sel = 'tvshow', context=context_generos, thumbnail=config.get_thumb('genres'), fanart=fanart, text_color='thistle' ))

           itemlist.append(item.clone( channel='groups', action='mainlist', extra='groups', title='[B]Grupos[/B]', context=context_cfg_search, thumbnail=config.get_thumb('bookshelf'), fanart=fanart, text_color='magenta' ))

        if config.get_setting('mnu_generos', default=True):
           itemlist.append(item.clone( channel='generos', action='mainlist', title= '[B]Géneros[/B]', tip_sel = 'tvshow', context=context_generos, thumbnail=config.get_thumb('genres'), fanart=fanart, text_color='thistle' ))

        item.category = 'Canales con Series'
        itemlist.append(item.clone( action='', title='[B]- [I]Series:[/I][/B]', context=context_usual, plot=item.category, thumbnail=config.get_thumb('tvshow'), fanart=fanart, text_color='hotpink' ))

        accion = 'mainlist_series'
        filtros = {'categories': 'tvshow'}

    elif item.extra == 'documentaries':
        if config.get_setting('mnu_search_proxy_channels', default=False):
            itemlist.append(item.clone( channel='submnuctext', action='submnu_search', title='[B]Buscar Nuevos Proxies[/B]', context=context_proxy_channels, only_options_proxies = True, thumbnail=config.get_thumb('flame'), fanart=fanart, text_color='red' ))

        if config.get_setting('sub_mnu_favoritos', default=False):
            itemlist.append(item.clone( channel='favoritos', action='mainlist', title='[B]Favoritos[/B]', context=context_cfg_search, thumbnail=config.get_thumb('star'), fanart=fanart, text_color='plum' ))

        if config.get_setting('sub_mnu_special', default=True):
            itemlist.append(item.clone( channel='submnuctext', action='submnu_special', title='[B]Especiales[/B]', context=context_cfg_search, extra='documentaries', thumbnail=config.get_thumb('heart'), fanart=fanart, text_color='pink' ))

        itemlist.append(item.clone( channel='submnuctext', action='submnu_channels', title='[B]Buscar[/B]', context=context_buscar, extra = 'documentaries', thumbnail=config.get_thumb('search'), fanart=fanart, text_color='yellow' ))

        if config.get_setting('mnu_grupos', default=True):
            itemlist.append(item.clone( channel='groups', action='mainlist', extra='groups', title='[B]Grupos[/B]', context=context_cfg_search, thumbnail=config.get_thumb('bookshelf'), fanart=fanart, text_color='magenta' ))

        if config.get_setting('mnu_generos', default=True):
           itemlist.append(item.clone( channel='generos', action='mainlist', title= '[B]Géneros[/B]', tip_sel = 'movie', context=context_generos, thumbnail=config.get_thumb('genres'), fanart=fanart, text_color='thistle' ))

        itemlist.append(item.clone( channel='groups', action='ch_groups', title = '[COLOR cyan][B]Todos[/B][/COLOR] los canales con temática Documental', group = 'docs', thumbnail=config.get_thumb('documentary'), fanart=fanart ))

        item.category = 'Canales con Documentales'
        itemlist.append(item.clone( action='', title='[B]- [I]Documentales:[/I][/B]', context=context_usual, plot=item.category, thumbnail=config.get_thumb('documentary'), fanart=fanart, text_color='cyan' ))

        accion = 'mainlist'
        filtros = {'categories': 'documentary'}

    elif item.extra == 'mixed':
        if config.get_setting('mnu_search_proxy_channels', default=False):
            itemlist.append(item.clone( channel='submnuctext', action='submnu_search', title='[B]Buscar Nuevos Proxies[/B]', context=context_proxy_channels, only_options_proxies = True, thumbnail=config.get_thumb('flame'), fanart=fanart, text_color='red' ))

        if config.get_setting('sub_mnu_favoritos', default=False):
            itemlist.append(item.clone( channel='favoritos', action='mainlist', title='[B]Favoritos[/B]', context=context_cfg_search, thumbnail=config.get_thumb('star'), fanart=fanart, text_color='plum' ))

        if config.get_setting('sub_mnu_news', default=True):
            itemlist.append(item.clone( channel='submnuctext', action='submnu_news', title='[B]Novedades[/B]', context=context_cfg_search, extra = 'mixed', thumbnail=config.get_thumb('novedades'), fanart=fanart, text_color='darksalmon' ))

        if config.get_setting('sub_mnu_special', default=True):
            itemlist.append(item.clone( channel='submnuctext', action='submnu_special', title='[B]Especiales[/B]', context=context_cfg_search, extra='all', no_docs = item.no_docs, thumbnail=config.get_thumb('heart'), fanart=fanart, text_color='pink' ))

        itemlist.append(item.clone( channel='submnuctext', action='submnu_channels', title='[B]Buscar[/B]', context=context_buscar, extra = 'mixed', thumbnail=config.get_thumb('search'), fanart=fanart, text_color='yellow' ))

        if config.get_setting('mnu_grupos', default=True):
            itemlist.append(item.clone( channel='groups', action='mainlist', extra='groups', title='[B]Grupos[/B]', context=context_cfg_search, thumbnail=config.get_thumb('bookshelf'), fanart=fanart, text_color='magenta' ))

        if config.get_setting('mnu_generos', default=True):
            itemlist.append(item.clone( channel='generos', action='mainlist', title= '[B]Géneros[/B]', tip_sel = 'all', context=context_generos, thumbnail=config.get_thumb('genres'), fanart=fanart, text_color='thistle' ))

        item.category = 'Canales con Películas y Series (ambos contenidos)'
        itemlist.append(item.clone( action='', title='[B]- [I]Películas y Series:[/I][/B]', context=context_usual, plot=item.category, thumbnail=config.get_thumb('booklet'), fanart=fanart, text_color='teal' ))

        accion = 'mainlist'
        filtros = {}

    elif item.extra == 'torrents':
        cliente_torrent = config.get_setting('cliente_torrent', default='Seleccionar')

        if cliente_torrent == 'Seleccionar' or cliente_torrent == 'Ninguno':
            itemlist.append(item.clone( channel='actions', action='open_settings', title='[COLOR chocolate][B]Ajustes[/B][/COLOR] preferencias (categoría [COLOR blue][B]Torrents)[/B][/COLOR]' + ' [COLOR fuchsia][B]Motor:[/B][/COLOR][COLOR goldenrod][B] ' + cliente_torrent.capitalize() + '[/B][/COLOR]', folder=False, thumbnail=config.get_thumb('settings'), fanart=fanart ))

        if config.get_setting('mnu_search_proxy_channels', default=False):
            itemlist.append(item.clone( channel='submnuctext', action='submnu_search', title='[B]Buscar Nuevos Proxies[/B]', context=context_proxy_channels, only_options_proxies = True, thumbnail=config.get_thumb('flame'), fanart=fanart, text_color='red' ))

        if config.get_setting('sub_mnu_favoritos', default=False):
            itemlist.append(item.clone( channel='favoritos', action='mainlist', title='[B]Favoritos[/B]', context=context_cfg_search, thumbnail=config.get_thumb('star'), fanart=fanart, text_color='plum' ))

        itemlist.append(item.clone( channel='submnuctext', action='submnu_channels', title='[B]Buscar[/B]', context=context_buscar, extra = 'torrents', thumbnail=config.get_thumb('search'), fanart=fanart, text_color='yellow' ))

        if config.get_setting('mnu_generos', default=True):
           itemlist.append(item.clone( channel='generos', action='mainlist', title= '[B]Géneros[/B]', tip_sel = 'movie', context=context_generos, thumbnail=config.get_thumb('genres'), fanart=fanart, text_color='thistle' ))

        itemlist.append(item.clone( channel='groups', action='ch_groups', title = '[COLOR blue][B]Canales[/B][/COLOR] que pueden tener enlaces Torrents', group = 'torrents',  thumbnail=config.get_thumb('stack'), fanart=fanart ))

        item.category = 'Canales con archivos Torrents'
        itemlist.append(item.clone( action='', title='[B]- [I]Torrents:[/I][/B]', context=context_torrents, plot=item.category, thumbnail=config.get_thumb('torrents'), fanart=fanart, text_color='blue' ))

        accion = 'mainlist'
        filtros = {'categories': 'torrent'}

    else:
        if item.extra == 'adults': pass
        elif item.extra == 'anime': pass
        elif item.extra == 'dorama': pass
        elif item.extra == 'infantil': pass
        elif item.extra == 'tales': pass

        elif not item.extra == 'groups':
            presentar = True

            if config.get_setting('mnu_proxies', default=False):
                if item.extra == 'proxies': presentar = False

            if config.get_setting('mnu_clones', default=False):
                if item.extra == 'clones': presentar = False

            if config.get_setting('mnu_problematicos', default=False):
                if item.extra == 'problematics': presentar = False

            if config.get_setting('mnu_desactivados', default=False):
                if item.extra == 'disableds': presentar = False

            if presentar:
               if config.get_setting('mnu_search_proxy_channels', default=False):
                   itemlist.append(item.clone( channel='submnuctext', action='submnu_search', title='[B]Buscar Nuevos Proxies[/B]', context=context_proxy_channels, only_options_proxies = True, thumbnail=config.get_thumb('flame'), fanart=fanart, text_color='red' ))

               if config.get_setting('sub_mnu_favoritos', default=False):
                   itemlist.append(item.clone( channel='favoritos', action='mainlist', title='[B]Favoritos[/B]', context=context_cfg_search, thumbnail=config.get_thumb('star'), fanart=fanart, text_color='plum' ))

               if config.get_setting('sub_mnu_news', default=True):
                   itemlist.append(item.clone( channel='submnuctext', action='submnu_news', title='[B]Novedades[/B]', context=context_cfg_search, extra = 'mixed', thumbnail=config.get_thumb('novedades'), fanart=fanart, text_color='darksalmon' ))

               if config.get_setting('sub_mnu_special', default=True):
                   itemlist.append(item.clone( channel='submnuctext', action='submnu_special', title='[B]Especiales[/B]', context=context_cfg_search, extra='all', thumbnail=config.get_thumb('heart'), fanart=fanart, text_color='pink' ))

               itemlist.append(item.clone( channel='submnuctext', action='submnu_channels', title='[B]Buscar[/B]', context=context_buscar, extra = 'all', thumbnail=config.get_thumb('search'), fanart=fanart, text_color='yellow' ))

               if config.get_setting('mnu_grupos', default=True):
                   itemlist.append(item.clone( channel='groups', action='mainlist', extra='groups', title='[B]Grupos[/B]', context=context_cfg_search, thumbnail=config.get_thumb('bookshelf'), fanart=fanart, text_color='magenta' ))

               if config.get_setting('mnu_generos', default=True):
                   itemlist.append(item.clone( channel='generos', action='mainlist', title= '[B]Géneros[/B]', tip_sel = 'all', context=context_generos, thumbnail=config.get_thumb('genres'), fanart=fanart, text_color='thistle' ))

        if item.extra == 'adults': item.category = 'Solo los Canales exclusivos para Adultos'
        elif item.extra == 'anime': item.category = 'Solo los Canales exclusivos de Animes'
        elif item.extra == 'dorama': item.category = 'Solo los Canales exclusivos de Doramas'
        elif item.extra == 'infantil': item.category = 'Solo los Canales exclusivos Infantiles'
        elif item.extra == 'tales': item.category = 'Solo los Canales con temática de Novelas'

        elif item.extra == 'suggested':
           item.category = 'Solo los Canales Sugeridos'
           itemlist.append(item.clone( action='', title='[B]- [I]Sugeridos:[/I][/B]', context=context_usual, plot=item.category, thumbnail=config.get_thumb('suggested'), fanart=fanart, text_color='aquamarine' ))

        elif item.extra == 'proxies': item.category = 'Solo los Canales con Proxies Memorizados'
        elif item.extra == 'clones': item.category = 'Solo los Canales que sean Clones'

        elif item.extra == 'disableds': item.category = 'Solo los Canales que estén Desactivados'

        elif item.extra == 'problematics': item.category = 'Solo los Canales que sean Problemáticos (Predominan Sin enlaces Disponibles/Válidos/Soportados)'

        elif not item.extra == 'groups':
           if item.extra == 'prefereds':
               item.category = 'Solo los Canales Preferidos'
               itemlist.append(item.clone( action='', title='[B]- [I]Canales Preferidos:[/I][/B]', context=context_usual, plot=item.category, thumbnail=config.get_thumb('stack'), fanart=fanart, text_color='coral' ))
           else:
               item.category = 'Todos los Canales'
               itemlist.append(item.clone( action='', title='[B]- [I]Canales:[/I][/B]', context=context_usual, plot=item.category, thumbnail=config.get_thumb('stack'), fanart=fanart, text_color='gold' ))

        else: item.category = 'Canales con Agrupaciones (Novedades, Estrenos, Temáticas, Países, Años, Plataformas, Productoras, Géneros, etc.)'

        if item.extra == 'infantil':
            if config.get_setting('mnu_search_proxy_channels', default=False):
                itemlist.append(item.clone( channel='submnuctext', action='submnu_search', title='[B]Buscar Nuevos Proxies[/B]', context=context_proxy_channels, only_options_proxies = True, thumbnail=config.get_thumb('flame'), fanart=fanart, text_color='red' ))

            if config.get_setting('sub_mnu_favoritos', default=False):
                itemlist.append(item.clone( channel='favoritos', action='mainlist', title='[B]Favoritos[/B]', context=context_cfg_search, thumbnail=config.get_thumb('star'), fanart=fanart, text_color='plum' ))

            if config.get_setting('sub_mnu_special', default=True):
                itemlist.append(item.clone( channel='submnuctext', action='submnu_special', title='[B]Especiales[/B]', context=context_cfg_search, extra='infantil', thumbnail=config.get_thumb('heart'), fanart=fanart, text_color='pink' ))

            itemlist.append(item.clone( channel='submnuctext', action='submnu_channels', title='[B]Buscar[/B]', context=context_buscar, extra = 'infantil', thumbnail=config.get_thumb('search'), fanart=fanart, text_color='yellow' ))

            if config.get_setting('mnu_grupos', default=True):
                itemlist.append(item.clone( channel='groups', action='mainlist', extra='groups', title='[B]Grupos[/B]', context=context_cfg_search, thumbnail=config.get_thumb('bookshelf'), fanart=fanart, text_color='magenta' ))

            if config.get_setting('mnu_generos', default=True):
                itemlist.append(item.clone( channel='generos', action='mainlist', title= '[B]Géneros[/B]', tip_sel = 'all', context=context_generos, thumbnail=config.get_thumb('genres'), fanart=fanart, text_color='thistle' ))

            itemlist.append(item.clone( channel='groups', action='ch_groups', title = '[COLOR tan][B]Todos[/B][/COLOR][B] los canales con contenido Infantil[/B]', group = 'kids', fanart=fanart ))

            itemlist.append(item.clone( action='', title='[B]- [I]Infantiles:[/I][/B]', context=context_usual, plot=item.category, thumbnail=config.get_thumb('booklet'), fanart=fanart, text_color='lightyellow' ))

        if item.extra == 'tales':
            if config.get_setting('mnu_search_proxy_channels', default=False):
                itemlist.append(item.clone( channel='submnuctext', action='submnu_search', title='[B]Buscar Nuevos Proxies[/B]', context=context_proxy_channels, only_options_proxies = True, thumbnail=config.get_thumb('flame'), fanart=fanart, text_color='red' ))

            if config.get_setting('sub_mnu_favoritos', default=False):
                itemlist.append(item.clone( channel='favoritos', action='mainlist', title='[B]Favoritos[/B]', context=context_cfg_search, thumbnail=config.get_thumb('star'), fanart=fanart, text_color='plum' ))

            itemlist.append(item.clone( channel='submnuctext', action='submnu_channels', title='[B]Buscar[/B]', context=context_buscar, extra = 'tales', thumbnail=config.get_thumb('search'), fanart=fanart, text_color='yellow' ))

            itemlist.append(item.clone( channel='groups', action='ch_groups', title = '[COLOR limegreen][B]Todos[/B][/COLOR][B] los canales con contenido de Novelas[/B]', group = 'tales', fanart=fanart ))

            itemlist.append(item.clone( action='', title='[B]- [I]Novelas:[/I][/B]', context=context_usual, plot=item.category, thumbnail=config.get_thumb('booklet'), fanart=fanart, text_color='limegreen' ))

        if item.extra == 'dorama':
            if config.get_setting('mnu_search_proxy_channels', default=False):
                itemlist.append(item.clone( channel='submnuctext', action='submnu_search', title='[B]Buscar Nuevos Proxies[/B]', context=context_proxy_channels, only_options_proxies = True, thumbnail=config.get_thumb('flame'), fanart=fanart, text_color='red' ))

            if config.get_setting('sub_mnu_favoritos', default=False):
                itemlist.append(item.clone( channel='favoritos', action='mainlist', title='[B]Favoritos[/B]', context=context_cfg_search, thumbnail=config.get_thumb('star'), fanart=fanart, text_color='plum' ))

            itemlist.append(item.clone( channel='submnuctext', action='submnu_channels', title='[B]Buscar[/B]', context=context_buscar, extra = 'dorama', thumbnail=config.get_thumb('search'), fanart=fanart, text_color='yellow' ))

            itemlist.append(item.clone( channel='groups', action='ch_groups', title = '[COLOR firebrick][B]Todos[/B][/COLOR] los canales con contenido Dorama', group = 'dorama', fanart=fanart ))

            itemlist.append(item.clone( action='', title='[B]- [I]Doramas:[/I][/B]', context=context_usual, plot=item.category, thumbnail=config.get_thumb('computer'), fanart=fanart, text_color='firebrick' ))

        if item.extra == 'adults' or item.extra == 'anime':
            if not config.get_setting('adults_password'):
                itemlist.append(item.clone( channel='helper', action='show_help_adults', title='[COLOR green][B]Información [COLOR goldenrod]Parental[/B][/COLOR]', thumbnail=config.get_thumb('news'), fanart=fanart ))

                presentar = True

                if item.extra == 'anime':
                    if not config.get_setting('animes_password'): presentar = False

                if presentar:
                    itemlist.append(item.clone( channel='actions', action='adults_password', title= '[COLOR goldenrod][B]Establecer[/B][/COLOR] un PIN Parental', thumbnail=config.get_thumb('pencil'), fanart=fanart ))
            else:
                presentar = True

                if item.extra == 'anime':
                    if not config.get_setting('animes_password'): presentar = False

                if presentar:
                    itemlist.append(item.clone( channel='helper', action='show_pin_parental', title= '[COLOR springgreen][B]Ver[/B][/COLOR] el PIN Parental', thumbnail=config.get_thumb('pencil'), fanart=fanart ))

                    itemlist.append(item.clone( channel='actions', action='adults_password_del', title= '[COLOR red][B]Eliminar[/B][/COLOR] PIN parental', erase = True, folder=False, thumbnail=config.get_thumb('pencil'), fanart=fanart ))

            if item.extra == 'anime':
                if config.get_setting('mnu_search_proxy_channels', default=False):
                    itemlist.append(item.clone( channel='submnuctext', action='submnu_search', title='[B]Buscar Nuevos Proxies[/B]', context=context_proxy_channels, only_options_proxies = True, thumbnail=config.get_thumb('flame'), fanart=fanart, text_color='red' ))

            if config.get_setting('sub_mnu_favoritos', default=False):
                itemlist.append(item.clone( channel='favoritos', action='mainlist', title='[B]Favoritos[/B]', context=context_cfg_search, thumbnail=config.get_thumb('star'), fanart=fanart, text_color='plum' ))

            if item.extra == 'adults':
                itemlist.append(Item( channel='search', action='search', title='[B]Buscar [COLOR orange]vídeo[/COLOR][/B] ...', extra = '+18', search_video = 'adult', thumbnail=config.get_thumb('search'), fanart=fanart, text_color='yellow' ))

                itemlist.append(item.clone( channel='groups', action='ch_groups', title = '[COLOR orange][B]Todos[/B][/COLOR] los canales que pueden tener vídeos para Adultos', group = 'adults', pral = 'adults', thumbnail=config.get_thumb('stack'), fanart=fanart ))

                itemlist.append(item.clone( action='', title='[B]- [I]Adultos:[/I][/B]', context=context_adultos, plot=item.category, thumbnail=config.get_thumb('adults'), fanart=fanart, text_color='orange' ))

            if item.extra == 'anime':
                itemlist.append(item.clone( channel='submnuctext', action='submnu_channels', title='[B]Buscar[/B]', context=context_buscar, extra = 'anime', thumbnail=config.get_thumb('search'), fanart=fanart, text_color='yellow' ))

                itemlist.append(item.clone( channel='groups', action='ch_groups', title = '[COLOR springgreen][B]Todos[/B][/COLOR] los canales con contenido Anime', group = 'anime', thumbnail=config.get_thumb('stack'), fanart=fanart  ))

                itemlist.append(item.clone( action='', title='[B]- [I]Animes:[/I][/B]', context=context_parental, plot=item.category, thumbnail=config.get_thumb('anime'), fanart=fanart, text_color='springgreen' ))

        if item.extra == 'proxies' or item.extra == 'clones' or item.extra == 'problematics' or item.extra == 'disableds':
            itemlist.append(item.clone( channel='actions', action='open_settings', title='[COLOR chocolate][B]Ajustes[/B][/COLOR] preferencias (categoría [COLOR tan][B]Menú)[/B][/COLOR]', context=context_config, folder=False, thumbnail=config.get_thumb('settings'), fanart=fanart ))

            if item.extra == 'proxies':
                itemlist.append(item.clone( action='', title='[B]- [I]Proxies:[/I][/B]', context=context_proxy_channels, plot=item.category, thumbnail=config.get_thumb('stack'), fanart=fanart, text_color='red' ))

            if item.extra == 'clones':
                itemlist.append(item.clone( action='', title='[B]- [I]Clones:[/I][/B]', context=context_proxy_channels, plot=item.category, thumbnail=config.get_thumb('stack'), fanart=fanart, text_color='turquoise' ))

            if item.extra == 'problematics':
                itemlist.append(item.clone( action='', title='[B]- [I]Problemáticos:[/I][/B]', context=context_desactivados, plot=item.category, thumbnail=config.get_thumb('stack'), fanart=fanart, text_color='darkgoldenrod' ))

            if item.extra == 'disableds':
                itemlist.append(item.clone( action='', title='[B]- [I]Desactivados:[/I][/B]', context=context_desactivados, plot=item.category, thumbnail=config.get_thumb('stack'), fanart=fanart, text_color='gray' ))

        accion = 'mainlist'
        filtros = {}

    channels_list_status = config.get_setting('channels_list_status', default=0)
    if channels_list_status > 0:
        filtros['status'] = 0 if channels_list_status == 1 else 1

    ch_list = channeltools.get_channels_list(filtros=filtros)

    i = 0

    for ch in ch_list:
        cfg_proxies_channel = 'channel_' + ch['id'] + '_proxies'

        if not item.extra == 'all':
            if 'dedicada exclusivamente a los tráilers' in ch['notes']: continue

        if item.extra == 'prefereds':
            if not ch['status'] == 1: continue

        if item.extra == 'problematics':
            if not 'problematic' in ch['clusters']: continue
        else:
            if not item.extra == 'all':
                if config.get_setting('mnu_problematicos', default=False):
                    if 'problematic' in ch['clusters']: continue

        if item.extra == 'disableds':
            if not ch['status'] == -1: continue
        else:
            if not item.extra == 'all':
                if config.get_setting('mnu_desactivados', default=False):
                    if ch['status'] == -1: continue

        if item.extra == 'proxies':
            if not 'Puede requerir el uso de proxies' in ch['notes']: continue

            if not config.get_setting(cfg_proxies_channel, default=''): continue

        if item.extra == 'clones':
            if not 'clone' in ch['clusters']: continue

        else:
            if not item.extra == 'all':
                if item.extra == 'proxies': pass
                elif item.extra == 'clones': pass

                elif not item.extra == 'disableds':
                    if config.get_setting('mnu_proxies', default=False):
                        if 'Puede requerir el uso de proxies' in ch['notes']:
                            if config.get_setting(cfg_proxies_channel, default=''): continue

                    if config.get_setting('mnu_clones', default=False):
                        if 'clone' in ch['clusters']: continue

        if item.extra == 'movies':
            if ch['searchable'] == False:
                if 'adults' in ch['clusters']: continue
                elif 'anime' in ch['clusters']:
                   if config.get_setting('mnu_animes', default=True): continue
                elif 'dorama' in ch['clusters']:
                   if config.get_setting('mnu_doramas', default=True): continue
                elif 'infantil' in ch['clusters']:
                   if config.get_setting('mnu_infantiles', default=True): continue
                elif 'tales' in ch['clusters']:
                   if config.get_setting('mnu_novelas', default=True): continue

        elif item.extra == 'tvshows':
            if ch['searchable'] == False:
                if 'adults' in ch['clusters']: continue
                elif 'mangas' in ch['notes'].lower(): continue
                elif 'anime' in ch['clusters']:
                   if config.get_setting('mnu_animes', default=True): continue
                elif 'dorama' in ch['clusters']:
                   if config.get_setting('mnu_doramas', default=True): continue

                elif 'infantil' in ch['clusters']:
                   if not ch['id'] == 'seodiv':
                       if config.get_setting('mnu_infantiles', default=True): continue

                elif 'tales' in ch['clusters']:
                   if config.get_setting('mnu_novelas', default=True): continue

        elif item.extra == 'adults':
            if ch['searchable'] == True: continue
            if not 'adults' in ch['clusters']: continue

        elif item.extra == 'anime':
            if ch['searchable'] == True: continue
            if not 'anime' in ch['clusters']: continue

        elif item.extra == 'mixed':
            tipos = ch['search_types']
            if 'documentary' in tipos: continue

            if not 'movie' in tipos: continue
            if not 'tvshow' in tipos: continue

        elif item.extra == 'torrents':
            if 'Streaming y Torrent' in ch['notes']: continue

            tipos = ch['search_types']
            if 'documentary' in tipos: continue

        elif item.extra == 'suggested':
            if not 'suggested' in ch['clusters']: continue

            if config.get_setting('mnu_simple', default=False):
                if str(ch['search_types']) == "['documentary']": continue

            if not config.get_setting('mnu_documentales', default=True):
                if str(ch['search_types']) == "['documentary']": continue

            if not config.get_setting('mnu_novelas', default=True):
                if 'exclusivamente en novelas' in ch['notes']: continue

        elif item.extra == 'infantil':
            if not 'infantil' in ch['clusters']: continue

        elif item.extra == 'tales':
            if not 'tales' in ch['clusters']: continue

        elif item.extra == 'dorama':
            if ch['searchable'] == True: continue
            elif not 'dorama' in ch['clusters']: continue

        else:
           if config.get_setting('mnu_simple', default=False):
               if ch['searchable'] == False:
                   if 'adults' in ch['clusters']: continue
                   elif 'anime' in ch['clusters']: continue
                   elif 'dorama' in ch['clusters']: continue
                   elif 'infantil' in ch['clusters']: continue
                   elif 'tales' in ch['clusters']: continue
               else:
                   if str(ch['search_types']) == "['documentary']": continue
                   elif 'enlaces torrent exclusivamente' in ch['notes']: continue
                   elif 'dedicada exclusivamente al dorama' in ch['notes']: continue

                   elif not config.get_setting('mnu_documentales', default=True):
                       if str(ch['search_types']) == "['documentary']": continue

                   elif not config.get_setting('mnu_novelas', default=True):
                       if 'exclusivamente en novelas' in ch['notes']: continue

           else:
              if not config.get_setting('mnu_documentales', default=True):
                  if str(ch['search_types']) == "['documentary']": continue

              if not config.get_setting('mnu_infantiles', default=True):
                  if 'infantil' in ch['clusters']: continue

              if not config.get_setting('mnu_novelas', default=True):
                  if 'exclusivamente en novelas' in ch['notes']: continue
                  elif 'tales' in ch['clusters']: continue

              if not config.get_setting('mnu_torrents', default=True):
                  if 'enlaces torrent exclusivamente' in ch['notes']: continue

              if not config.get_setting('mnu_doramas', default=True):
                  if ch['searchable'] == False: continue
                  elif 'dorama' in ch['clusters']: continue

              if not config.get_setting('mnu_animes', default=True):
                  if ch['searchable'] == False: continue
                  elif 'anime' in ch['clusters']: continue

              if not config.get_setting('mnu_adultos', default=True):
                  if ch['searchable'] == False: continue
                  elif 'adults' in ch['clusters']: continue

        context = []

        if 'proxies' in ch['notes'].lower():
            if config.get_setting(cfg_proxies_channel, default=''):
                tit = '[COLOR %s]Quitar Proxies del Canal[/COLOR]' % color_list_proxies
                context.append({'title': tit, 'channel': item.channel, 'action': '_quitar_proxies'})

        if ch['searchable']:
            if not ch['status'] == -1:
                cfg_searchable_channel = 'channel_' + ch['id'] + '_no_searchable'

                if config.get_setting(cfg_searchable_channel, default=False):
                    tit = '[COLOR %s][B]Quitar Excluido Búsquedas[/B][/COLOR]' % color_adver
                    context.append({'title': tit, 'channel': item.channel, 'action': '_quitar_no_searchables'})
                else:
                    if config.get_setting('search_included_all', default=''):
                        search_included_all = config.get_setting('search_included_all')

                        el_memorizado = "'" + ch['id'] + "'"
                        if el_memorizado in str(search_included_all):
                            tit = '[COLOR indianred][B]Quitar Búsquedas Solo en[/B][/COLOR]'
                            context.append({'title': tit, 'channel': 'submnuctext', 'action': '_channels_included_del_one'})

                    if config.get_setting('search_excludes_all', default=''):
                        search_excludes_all = config.get_setting('search_excludes_all')

                        el_memorizado = "'" + ch['id'] + "'"
                        if el_memorizado in str(search_excludes_all):
                            tit = '[COLOR indianred][B]Quitar Exclusión Búsquedas[/B][/COLOR]'
                            context.append({'title': tit, 'channel': 'submnuctext', 'action': '_channels_excluded_del'})


                    elif config.get_setting('search_excludes_movies', default=''):
                        search_excludes_movies = config.get_setting('search_excludes_movies')

                        el_memorizado = "'" + ch['id'] + "'"
                        if el_memorizado in str(search_excludes_movies):
                            tit = '[B][COLOR deepskyblue]Películas [COLOR indianred]Quitar Exclusión Búsquedas[/B][/COLOR]'
                            context.append({'title': tit, 'channel': 'submnuctext', 'action': '_channels_excluded_del'})

                    elif config.get_setting('search_excludes_tvshows', default=''):
                        search_excludes_tvshows = config.get_setting('search_excludes_tvshows')

                        el_memorizado = "'" + ch['id'] + "'"
                        if el_memorizado in str(search_excludes_tvshows):
                            tit = '[B][COLOR hotpink]Series [COLOR indianred]Quitar Exclusión Búsquedas[/B][/COLOR]'
                            context.append({'title': tit, 'channel': 'submnuctext', 'action': '_channels_excluded_del'})

                    elif config.get_setting('search_excludes_documentaries', default=''):
                        search_excludes_documentaries = config.get_setting('search_excludes_documentaries')

                        el_memorizado = "'" + ch['id'] + "'"
                        if el_memorizado in str(search_excludes_documentaries):
                            tit = '[B][COLOR cyan]Documentales [COLOR indianred]Quitar Exclusión Búsquedas[/B][/COLOR]'
                            context.append({'title': tit, 'channel': 'submnuctext', 'action': '_channels_excluded_del'})

                    elif config.get_setting('search_excludes_torrents', default=''):
                        search_excludes_torrents = config.get_setting('search_excludes_torrents')

                        el_memorizado = "'" + ch['id'] + "'"
                        if el_memorizado in str(search_excludes_torrents):
                            tit = '[B][COLOR blue]Torrents [COLOR indianred]Quitar Exclusión Búsquedas[/B][/COLOR]'
                            context.append({'title': tit, 'channel': 'submnuctext', 'action': '_channels_excluded_del'})

                    elif config.get_setting('search_excludes_mixed', default=''):
                        search_excludes_mixed = config.get_setting('search_excludes_mixed')

                        el_memorizado = "'" + ch['id'] + "'"
                        if el_memorizado in str(search_excludes_mixed):
                            tit = '[B][COLOR teal]Películas y/ó Series [COLOR indianred]Quitar Exclusión Búsquedas[/B][/COLOR]'
                            context.append({'title': tit, 'channel': 'submnuctext', 'action': '_channels_excluded_del'})

                    else:
                        tit = '[COLOR %s][B]Excluir en Búsquedas[/B][/COLOR]' % color_adver
                        context.append({'title': tit, 'channel': item.channel, 'action': '_poner_no_searchables'})

        if ch['status'] != 1:
            tit = '[COLOR %s][B]Marcar Canal como Preferido[/B][/COLOR]' % color_list_prefe
            context.append({'title': tit, 'channel': item.channel, 'action': '_marcar_canal', 'estado': 1})

        if ch['status'] != 0:
            if ch['status'] == 1:
                tit = '[COLOR %s][B]Des-Marcar Canal Preferido[/B][/COLOR]' % color_list_prefe
                context.append({'title': tit, 'channel': item.channel, 'action': '_marcar_canal', 'estado': 0})
            elif ch['status'] == -1:
                tit = '[COLOR %s][B]Re-Activar Canal Desactivado[/B][/COLOR]' % color_list_inactive
                context.append({'title': tit, 'channel': item.channel, 'action': '_marcar_canal', 'estado': 0})
            else:
                tit = '[COLOR white][B]Marcar Canal como Activo[/B][/COLOR]'
                context.append({'title': tit, 'channel': item.channel, 'action': '_marcar_canal', 'estado': 0})

        if ch['status'] != -1:
            tit = '[COLOR %s][B]Marcar Canal como Desactivado[/B][/COLOR]' % color_list_inactive
            context.append({'title': tit, 'channel': item.channel, 'action': '_marcar_canal', 'estado': -1})

        cfg_domains = False

        if 'current' in ch['clusters']:
            cfg_domains = True

            tit = '[COLOR bisque]Gestión Dominios[/COLOR]'
            context.append({'title': tit, 'channel': 'helper', 'action': 'show_help_domains'})

        tit = '[COLOR %s][B]Últimos Cambios Dominios[/B][/COLOR]' % color_exec
        context.append({'title': tit, 'channel': 'actions', 'action': 'show_latest_domains'})

        if cfg_domains:
            tit = '[COLOR yellowgreen][B]Dominio Vigente[/B][/COLOR]'
            context.append({'title': tit, 'channel': item.channel, 'action': '_dominio_vigente'})

            if 'Dispone de varios posibles dominios' in ch['notes']:
                tit = '[COLOR powderblue][B]Configurar Dominio a usar[/B][/COLOR]'
                context.append({'title': tit, 'channel': item.channel, 'action': '_dominios'})

            tit = '[COLOR orange][B]Modificar Dominio Memorizado[/B][/COLOR]'
            context.append({'title': tit, 'channel': item.channel, 'action': '_dominio_memorizado'})

        if 'register' in ch['clusters']:
            cfg_user_channel = 'channel_' + ch['id'] + '_' + ch['id'] + '_username'
            cfg_pass_channel = 'channel_' + ch['id'] + '_' + ch['id'] + '_password'

            if not config.get_setting(cfg_user_channel, default='') or not config.get_setting(cfg_pass_channel, default=''):
                tit = '[COLOR green][B]Información Registrarse[/B][/COLOR]'
                context.append({'title': tit, 'channel': 'helper', 'action': 'show_help_register'})

                tit = '[COLOR teal][B]Credenciales Cuenta[/B][/COLOR]'
                context.append({'title': tit, 'channel': item.channel, 'action': '_credenciales'})
            else:
                cfg_login_channel = 'channel_' + ch['id'] + '_' + ch['id'] + '_login'

                presentar = True
                if 'dominios' in ch['notes'].lower():
                    cfg_dominio_channel = 'channel_' + ch['id'] + '_dominio'
                    if not config.get_setting(cfg_dominio_channel, default=''): presentar = False

                if presentar:
                    if config.get_setting(cfg_login_channel, default=False):
                        tit = '[COLOR teal][B]Cerrar Sesión[/B][/COLOR]'
                        context.append({'title': tit, 'channel': item.channel, 'action': '_credenciales'})

        if 'proxies' in ch['notes'].lower():
            if not config.get_setting(cfg_proxies_channel, default=''):
                tit = '[COLOR %s][B]Información Proxies[/B][/COLOR]' % color_infor
                context.append({'title': tit, 'channel': 'helper', 'action': 'show_help_proxies'})

            tit = '[COLOR %s][B]Configurar Proxies a usar[/B][/COLOR]' % color_list_proxies
            context.append({'title': tit, 'channel': item.channel, 'action': '_proxies'})

        if 'notice' in ch['clusters']:
            tit = '[COLOR tan][B]Aviso Canal[/B][/COLOR]'
            context.append({'title': tit, 'channel': 'helper', 'action': 'show_help_' + ch['id']})

        if 'register' in ch['clusters']:
            cfg_user_channel = 'channel_' + ch['id'] + '_' + ch['id'] + '_username'
            cfg_pass_channel = 'channel_' + ch['id'] + '_' + ch['id'] + '_password'

            if config.get_setting(cfg_user_channel, default='') and config.get_setting(cfg_pass_channel, default=''):
               cfg_login_channel = 'channel_' + ch['id'] + '_' + ch['id'] + '_login'

               if config.get_setting(cfg_login_channel, default=False):
                   cfg_dominio_channel = 'channel_' + ch['id'] + '_dominio'
                   tit = '[COLOR springgreen][B]Test Login Cuenta[/B][/COLOR]'
                   context.append({'title': tit, 'channel': 'submnuctext', 'action': '_credenciales_' + ch['id']})

        tit = '[COLOR darkorange][B]Test Web Canal[/B][/COLOR]'
        context.append({'title': tit, 'channel': item.channel, 'action': '_tests'})

        if cfg_domains:
            tit = '[COLOR %s]Ajustes categoría Dominios[/COLOR]' % color_exec
            context.append({'title': tit, 'channel': 'actions', 'action': 'open_settings'})

        color = color_list_prefe if ch['status'] == 1 else 'white' if ch['status'] == 0 else color_list_inactive

        plot = ''
        if item.extra == 'all': plot += '[' + ', '.join([config.get_localized_category(ct) for ct in ch['categories']]) + '][CR]'
        plot += '[' + ', '.join([idioma_canal(lg) for lg in ch['language']]) + ']'
        if ch['notes'] != '': plot += '[CR][CR]' + ch['notes']

        titulo = ch['name']

        if ch['status'] == -1:
            if not item.extra == 'disableds': titulo += '[I][B][COLOR %s] (desactivado)[/COLOR][/I][/B]' % color_list_inactive
            if config.get_setting(cfg_proxies_channel, default=''): titulo += '[I][B][COLOR %s] (proxies)[/COLOR][/I][/B]' % color_list_proxies
        else:
            if ch['status'] == 1:
               if not item.extra == 'prefereds': titulo += '[I][B][COLOR wheat] (preferido)[/COLOR][/I][/B]'
            else:
                if not item.extra == 'suggested':
                    if 'suggested' in ch['clusters']: titulo += '[I][B][COLOR olivedrab] (sugerido)[/COLOR][/I][/B]'

            if config.get_setting(cfg_proxies_channel, default=''):
                if ch['status'] == 1: titulo += '[I][B][COLOR %s] (proxies)[/COLOR][/I][/B]' % color_list_proxies
                else: color = color_list_proxies

        if 'register' in ch['clusters']:
            cfg_user_channel = 'channel_' + ch['id'] + '_' + ch['id'] + '_username'
            cfg_pass_channel = 'channel_' + ch['id'] + '_' + ch['id'] + '_password'

            if not config.get_setting(cfg_user_channel, default='') or not config.get_setting(cfg_pass_channel, default=''):
               titulo += '[I][B][COLOR teal] (cuenta)[/COLOR][/I][/B]'
            else:
               cfg_login_channel = 'channel_' + ch['id'] + '_' + ch['id'] + '_login'

               if config.get_setting(cfg_login_channel, default=False):
                   presentar = True
                   if 'dominios' in ch['notes'].lower():
                       cfg_dominio_channel = 'channel_' + ch['id'] + '_dominio'

                   if presentar: titulo += '[I][B][COLOR teal] (sesión)[/COLOR][/I][/B]'
               else: titulo += '[I][COLOR teal] (login)[/COLOR][/I]'

        if 'current' in ch['clusters']:
            cfg_current_channel = 'channel_' + ch['id'] + '_dominio'

            if config.get_setting(cfg_current_channel, default=False): titulo += '[I][B][COLOR green] (dominio)[/COLOR][/I][/B]'

        if 'inestable' in ch['clusters']:
            if config.get_setting('mnu_simple', default=False): continue
            elif config.get_setting('channels_list_no_inestables', default=False): continue

            titulo += '[I][B][COLOR plum] (inestable)[/COLOR][/I][/B]'

        elif 'problematic' in ch['clusters']:
            if config.get_setting('mnu_simple', default=False): continue

            if not item.extra == 'all':
                if not item.extra == 'problematics': 
                    if config.get_setting('mnu_problematicos', default=False): continue
                    elif config.get_setting('channels_list_no_problematicos', default=False): continue

            if not item.extra == 'problematics': titulo += '[I][B][COLOR darkgoldenrod] (problemático)[/COLOR][/I][/B]'

        elif 'clone' in ch['clusters']:
            if config.get_setting('mnu_simple', default=False): continue

            if not item.extra == 'all':
                if not item.extra == 'clones': 
                    if config.get_setting('mnu_clones', default=False): continue
                    elif config.get_setting('channels_list_no_clones', default=False): continue

            if not item.extra == 'clones': titulo += '[I][B][COLOR turquoise] (clon)[/COLOR][/I][/B]'

        if con_incidencias:
           if ch['name'] in str(con_incidencias): titulo += '[I][B][COLOR tan] (incidencia)[/COLOR][/I][/B]'

        if no_accesibles:
           if ch['name'] in str(no_accesibles): titulo += '[I][B][COLOR indianred] (no accesible)[/COLOR][/I][/B]'

        if con_problemas:
           if ch['name'] in str(con_problemas):
               hay_problemas = str(con_problemas).replace('[B][COLOR moccasin]', 'CHANNEL').replace('[COLOR lime]', '/CHANNEL')
               channels_con_problemas = scrapertools.find_multiple_matches(hay_problemas, "CHANNEL(.*?)/CHANNEL")

               for channel_con_problema in channels_con_problemas:
                    channel_con_problema = channel_con_problema.strip()

                    if not channel_con_problema == ch['name']: continue

                    titulo += '[I][B][COLOR tomato] (con problema)[/COLOR][/I][/B]'
                    break

        if ch['searchable']:
            if not ch['status'] == -1:
                cfg_searchable_channel = 'channel_' + ch['id'] + '_no_searchable'

                if config.get_setting(cfg_searchable_channel, default=False): titulo += '[I][B][COLOR yellowgreen] (no búsquedas)[/COLOR][/I][/B]'

                if config.get_setting('search_included_all', default=''):
                   if ch['id'] in str(config.get_setting('search_included_all')): titulo += '[I][B][COLOR yellowgreen] (solo buscar)[/COLOR][/I][/B]'

        presentar = False

        if config.get_setting('mnu_simple', default=False): presentar = True
        elif config.get_setting('channels_link_main', default=True): presentar = True

        if not item.detallar: presentar = False

        if presentar:
            if not config.get_setting('mnu_adultos', default=True):
                if '+18' in ch['notes']: continue

            if 'movie' in ch['categories']:
                if 'tvshow' in ch['categories']:
                    titulo += '[B][I][COLOR deepskyblue] películas[/COLOR] [COLOR hotpink]series[/COLOR][/I][/B]'
                    if 'tales' in ch['clusters']: titulo += '[B][I][COLOR limegreen] novelas[/COLOR][/I][/B]'
                else:
                    if '+18' in ch['notes']: titulo += '[B][I][COLOR orange] +18[/COLOR][/I][/B]'
                    else: titulo += '[B][I][COLOR deepskyblue] películas[/COLOR][/I][/B]'
            else:
                if 'tvshow' in ch['categories']:
                    titulo += '[B][I][COLOR hotpink] series[/COLOR][/I][/B]'
                    if 'tales' in ch['clusters']: titulo += '[B][I][COLOR limegreen] novelas[/COLOR][/I][/B]'
                elif "documentary" in ch['categories']: titulo += '[B][I][COLOR cyan] documentales[/COLOR][/I][/B]'

        i += 1 

        itemlist.append(Item( channel=ch['id'], action=accion, title=titulo, context=context, text_color=color, plot=plot, extra=item.extra, thumbnail=ch['thumbnail'], fanart=fanart, category=ch['name'] ))

    if len(ch_list) == 0 or i == 0:
        if item.extra == 'Proxies' or item.extra == 'disableds':
            itemlist.append(item.clone( channel='actions', action='open_settings', title='[COLOR chocolate][B]Ajustes[/B][/COLOR] preferencias (categoría [COLOR tan][B]Menú)[/B][/COLOR]', context=context_config, folder=False, thumbnail=config.get_thumb('settings'), fanart=fanart ))

        if item.extra == 'proxies':
            itemlist.append(item.clone( channel='filters', action='with_proxies', title='[B]Sin canales con Proxies Memorizados[/B]', text_color=color_list_proxies, thumbnail=config.get_thumb('stack'), fanart=fanart, folder=False ))
        elif item.extra == 'clones':
            itemlist.append(item.clone( channel='filters', action='show_channels_list', title='[B]Sin canales Problemáticos[/B]', text_color='darkgoldenrod', problematics=True, thumbnail=config.get_thumb('stack'), fanart=fanart, folder=False ))
        elif item.extra == 'problematics':
            itemlist.append(item.clone( channel='filters', action='show_channels_list', title='[B]Sin canales Problemáticos[/B]', text_color='darkgoldenrod', clones=True, thumbnail=config.get_thumb('stack'), fanart=fanart, folder=False ))
        elif item.extra == 'disableds':
            itemlist.append(item.clone( channel='filters', action='channels_status', title='[B]Sin canales Desactivados[/B]', text_color=color_list_inactive, des_rea=True, thumbnail=config.get_thumb('stack'), fanart=fanart, folder=False ))
        else:
            itemlist.append(item.clone( channel='filters', action='channels_status', title='[B]Opción Sin canales[/B]', text_color=color_list_prefe, des_rea=False, thumbnail=config.get_thumb('stack'), fanart=fanart, folder=False ))

    return itemlist


def idioma_canal(lang):
    idiomas = { 'cast': 'Castellano', 'lat': 'Latino', 'eng': 'Inglés', 'pt': 'Portugués', 'vo': 'VO', 'vose': 'Vose', 'vos': 'Vos', 'cat': 'Català' }
    return idiomas[lang] if lang in idiomas else lang


def _marcar_canal(item):
    from modules import submnuctext
    submnuctext._marcar_canal(item)


def _poner_no_searchables(item):
    from modules import submnuctext
    submnuctext._poner_no_searchable(item)

def _quitar_no_searchables(item):
    from modules import submnuctext
    submnuctext._quitar_no_searchable(item)


def _quitar_proxies(item):
    from modules import submnuctext
    submnuctext._quitar_proxies(item)


def _dominio_vigente(item):
    from modules import submnuctext
    submnuctext._dominio_vigente(item)


def _dominio_memorizado(item):
    from modules import submnuctext
    submnuctext._dominio_memorizado(item)


def _dominios(item):
    from modules import submnuctext
    submnuctext._dominios(item)


def _credenciales(item):
    from modules import submnuctext
    submnuctext._credenciales(item)


def _proxies(item):
    from modules import submnuctext
    submnuctext._proxies(item)


def _tests(item):
    from modules import submnuctext
    submnuctext._test_webs(item)
    
# =========================================================================
# FUNCIONES AUXILIARES MENÚ AYUDA (BLOQUE COMPLETO)
# =========================================================================

def ayuda(item):
    logger.info()
    itemlist = []

    # 1. Tutorial de Uso (NUEVO)
    itemlist.append(item.clone( 
        action='tutorial_uso', 
        title='[B]¿Cómo funciona?[/B] (Tutorial Rápido)', 
        thumbnail=config.get_thumb('help'), 
        plot='Aprende los pasos básicos: Canal > Película > Servidor.'
    ))

    # 2. Telegram (Soporte)
    itemlist.append(item.clone( 
        action='show_telegram', 
        title='[B]Telegram de Soporte[/B]', 
        thumbnail=config.get_thumb('telegram'), # Asegúrate de tener telegram.png o usa 'help'
        plot='Escanea el código QR para unirte a nuestro grupo de ayuda.'
    ))

    # 3. Reportar Error (Log)
    itemlist.append(item.clone( 
        action='upload_log', 
        title='[B]Enviar Reporte de Fallo (Log)[/B]', 
        thumbnail=config.get_thumb('settings'), 
        plot='Sube tu registro de errores y genera un enlace para enviarlo al desarrollador.'
    ))

    # 4. Legalidad
    itemlist.append(item.clone( 
        action='show_legal', 
        title='[B]Legalidad[/B]', 
        thumbnail=config.get_thumb('info'), 
        plot='Información legal y de responsabilidad del addon.'
    ))

    # 5. Ajustes
    itemlist.append(item.clone( 
        channel='actions', 
        action='open_settings', 
        title='[B]Ajustes[/B]', 
        thumbnail=config.get_thumb('settings'), 
        plot='Configuración general del addon.'
    ))

    return itemlist

# --- FUNCIÓN 1: MOSTRAR TELEGRAM ---
def show_telegram(item):
    import xbmcgui
    from urllib.parse import quote

    # ¡¡¡ OJO: REVISA QUE AQUÍ ESTÉ TU ENLACE !!!
    mi_telegram = "https://t.me/TU_ENLACE_AQUI" 
    
    qr_url = "https://api.qrserver.com/v1/create-qr-code/?size=400x400&data=" + quote(mi_telegram)

    class QRDialog(xbmcgui.WindowDialog):
        def __init__(self):
            self.addControl(xbmcgui.ControlImage(480, 140, 960, 800, 'black')) 
            self.addControl(xbmcgui.ControlImage(760, 240, 400, 400, qr_url))
            self.addControl(xbmcgui.ControlLabel(480, 160, 960, 50, '[B][COLOR deepskyblue]Soporte en Telegram[/COLOR][/B]', alignment=6))
            self.addControl(xbmcgui.ControlLabel(480, 660, 960, 50, '[B]Escanea con tu móvil[/B]', alignment=6))
            self.addControl(xbmcgui.ControlLabel(480, 880, 960, 50, '[I]Pulsa cualquier tecla para cerrar[/I]', alignment=6))

        def onAction(self, action):
            self.close()
    
    dialog = QRDialog()
    dialog.doModal()
    del dialog
    return True

# --- FUNCIÓN 2: TUTORIAL DE USO (NUEVO) ---
def tutorial_uso(item):
    import xbmcgui
    
    txt = "[B][COLOR yellow]¿CÓMO VER UNA PELÍCULA O SERIE?[/COLOR][/B]\n\n"
    txt += "[B]1. ELIGE UN CANAL:[/B]\n"
    txt += "Los canales (ej. Filmaffinity, Cinecalidad...) son como 'páginas web'. Entra en el que más te guste.\n\n"
    txt += "[B]2. BUSCA EL CONTENIDO:[/B]\n"
    txt += "Navega por las listas o usa el Buscador hasta encontrar la carátula de lo que quieres ver.\n\n"
    txt += "[B]3. ELIGE EL SERVIDOR (El paso importante):[/B]\n"
    txt += "Al pinchar en la peli, verás una lista de 'enlaces' (ej: Gamovideo, Streamtape...).\n"
    txt += "- Pincha en uno.\n"
    txt += "- Si no carga, [B]prueba con el siguiente[/B].\n"
    txt += "- Los enlaces dependen de las webs externas. ¡Paciencia!\n\n"
    txt += "[B]CONSEJO:[/B] Los enlaces '1080p' se ven mejor pero requieren buena conexión."

    xbmcgui.Dialog().textviewer("Guía Rápida - ButacaVip", txt)
    return True

# --- FUNCIÓN 3: SUBIR LOG (REPORTE) ---
def upload_log(item):
    import xbmc, xbmcgui, os, socket
    
    # Localizar log según sistema
    if xbmc.getCondVisibility('system.platform.android'):
        log_path = os.path.join(xbmc.translatePath('special://logpath'), 'kodi.log')
    else:
        log_path = os.path.join(xbmc.translatePath('special://logpath'), 'kodi.log')

    if not os.path.exists(log_path):
        platformtools.dialog_notification("Error", "No hay log disponible")
        return

    if not xbmcgui.Dialog().yesno("Reportar Error", "¿Subir kodi.log para revisión?"): return

    try:
        with open(log_path, 'rb') as f: content = f.read()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect(('termbin.com', 9999))
        s.sendall(content)
        s.shutdown(socket.SHUT_WR)
        url = s.recv(1024).decode('utf-8').strip()
        s.close()
        
        xbmcgui.Dialog().ok("Log Subido", f"Pásame este enlace:\n[COLOR yellow]{url}[/COLOR]")
    except:
        xbmcgui.Dialog().ok("Error", "Fallo al subir el log.")

# --- FUNCIÓN 4: TEXTO LEGAL ---
def show_legal(item):
    import xbmcgui
    txt = '[B]Los Propietarios y Distribuidores de este Add-On no Proveen ni Distribuyen Ningún Contenido Mostrado por el Add-On.[/B]\n\n'
    txt += 'Está Prohibida su distribución junto con Contenidos Multimedia Protegidos.\n\n'
    txt += 'Si este contenido está Prohibido en su País, solamente Usted será el Responsable.\n\n'
    txt += '[B]Siendo el único Responsable quien lo haya Distribuido ó Utilizado Ilegalmente.[/B]'
    xbmcgui.Dialog().ok('Aviso Legal', txt)
    return True

def show_telegram(item):
    import xbmcgui
    from urllib.parse import quote

    # 1. Configura aquí tu usuario o grupo de Telegram
    mi_telegram = "https://t.me/ButacaVipSupport"  # Pon tu enlace real

    # 2. Usamos una API pública para generar el QR al vuelo (sin guardar imagen)
    # Esto evita tener que crear imágenes fijas. Genera el QR de la URL.
    qr_url = "https://api.qrserver.com/v1/create-qr-code/?size=400x400&data=" + quote(mi_telegram)

    # 3. Mostramos una ventana con la imagen
    class QRDialog(xbmcgui.WindowDialog):
        def __init__(self):
            # Fondo semitransparente
            self.addControl(xbmcgui.ControlImage(0, 0, 1920, 1080, ''))
            # Fondo negro central
            self.addControl(xbmcgui.ControlImage(480, 140, 960, 800, 'black')) 
            # El QR
            self.addControl(xbmcgui.ControlImage(760, 240, 400, 400, qr_url))
            # Texto explicativo
            self.addControl(xbmcgui.ControlLabel(0, 660, 1920, 50, '[B]ButacaVip - Escanea con tu móvil para entrar al Telegram[/B]', alignment=6)) # 6=Center
            self.addControl(xbmcgui.ControlLabel(0, 720, 1920, 50, 'Pulsa cualquier tecla para salir', alignment=6))

        def onAction(self, action):
            self.close()
    
    # Ejecutamos el diálogo
    dialog = QRDialog()
    dialog.doModal()
    del dialog
    
    return True

def tutorial_uso(item):
    import xbmcgui
    
    # Texto explicativo claro y sencillo
    txt = "[B][COLOR yellow]¿CÓMO VER UNA PELÍCULA O SERIE?[/COLOR][/B]\n\n"
    txt += "[B]1. ELIGE UN CANAL:[/B]\n"
    txt += "Los canales (ej. Filmaffinity, Cinecalidad...) son como 'páginas web'. Entra en el que más te guste.\n\n"
    txt += "[B]2. BUSCA EL CONTENIDO:[/B]\n"
    txt += "Navega por las listas (Estrenos, Géneros) o usa el Buscador hasta encontrar la carátula de lo que quieres ver.\n\n"
    txt += "[B]3. ELIGE EL SERVIDOR (El paso importante):[/B]\n"
    txt += "Al pinchar en la película, verás una lista de 'enlaces' o 'servidores' (ej: Gamovideo, Streamtape, Waaw...).\n"
    txt += "- Pincha en uno.\n"
    txt += "- Si no carga o da error, [B]prueba con el siguiente[/B].\n"
    txt += "- Los enlaces dependen de las webs, no de nosotros. ¡Paciencia!\n\n"
    txt += "[B]CONSEJO PRO:[/B] Los enlaces marcados como '1080p' o 'HD' se ven mejor, pero requieren mejor internet."

    # Usamos textviewer para que se pueda leer cómodamente
    xbmcgui.Dialog().textviewer("Guía Rápida - ButacaVip", txt)
    return True

def upload_log(item):
    import xbmc, xbmcgui, os, socket

    # 1. Localizar el log de Kodi
    if xbmc.getCondVisibility('system.platform.android'):
        log_path = os.path.join(xbmc.translatePath('special://logpath'), 'kodi.log')
    else:
        log_path = os.path.join(xbmc.translatePath('special://logpath'), 'kodi.log')

    if not os.path.exists(log_path):
        platformtools.dialog_notification("Error", "No se encuentra el archivo de Log")
        return

    # 2. Preguntar confirmación (Privacidad)
    confirm = xbmcgui.Dialog().yesno(
        "ButacaVip Reportar Error", 
        "Se va a subir tu archivo kodi.log a internet para revisarlo.\n"
        "No contiene contraseñas, pero sí rutas de archivos.\n"
        "¿Deseas continuar?"
    )
    if not confirm: return

    # 3. Leer y Subir el log (Usamos termbin.com porque es facilísimo por socket)
    try:
        platformtools.dialog_notification("Subiendo...", "Por favor espera")
        
        with open(log_path, 'rb') as f:
            content = f.read()
        
        # Conexión a termbin.com (puerto 9999)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect(('termbin.com', 9999))
        s.sendall(content)
        s.shutdown(socket.SHUT_WR)
        
        # Recibir respuesta (la URL)
        url = s.recv(1024).decode('utf-8').strip()
        s.close()

        # 4. Mostrar el resultado
        # Generamos un QR de la URL del log para que te lo puedan mandar fácil
        from urllib.parse import quote
        qr_url = "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=" + quote(url)
        
        # Mostramos cuadro con la URL escrita y el QR
        # (Aquí uso un Dialog simple para no complicar el código, pero podrías usar la clase QRDialog de arriba)
        xbmcgui.Dialog().ok("Log Subido Correctamente", f"Pásame este enlace por Telegram:\n\n[COLOR yellow]{url}[/COLOR]")
        
    except Exception as e:
        logger.error("Error subiendo log: " + str(e))
        xbmcgui.Dialog().ok("Error", "No se pudo subir el log. Revisa tu internet.")
