from django.shortcuts import render
from django.contrib.auth.decorators import login_required,user_passes_test
from tethys_sdk.gizmos import *
import csv, os
from datetime import datetime,timedelta
from tethys_sdk.services import get_spatial_dataset_engine
import urlparse
from grace import *
from utilities import *
import json,time
from .app import Grace
from model import *
from config import GRACE_NETCDF_DIR,GLOBAL_NETCDF_DIR,TOTAL_NETCDF_DIR,TOTAL_GLOBAL_NETCDF_DIR,SW_NETCDF_DIR,SW_GLOBAL_NETCDF_DIR,SOIL_NETCDF_DIR,SOIL_GLOBAL_NETCDF_DIR,GW_NETCDF_DIR,GW_GLOBAL_NETCDF_DIR
from updateGRACE import downloadFile

# NETCDF_DIR = GRACE_NETCDF_DIR

def home(request):
    """
    Controller for the app home page.
    """


    #Un-comment the following functions the first time you install the app and open the home page.  Comment them out again after all of the geotiffs have been created and uploaded.

    #------------------------------------------------------------------------------------

    # Total Storage GRACE Data
    # create_global_tiff_highres('/media/root/tethys/wmo_tethys-app/GRACE/tethysapp/grace/workspaces/app_workspace/gracedata/tot_/GRC_tot.25scaled.nc',"/Users/travismcstraw/tethysapps/GRACE/tethysapp/grace/workspaces/app_workspace/gracedata/tot_/global/geotiff_global/","lwe_thickness")
    # upload_global_tiff("/Users/travismcstraw/tethysapps/GRACE/tethysapp/grace/workspaces/app_workspace/gracedata/tot_/global/geotiff_global/","https://tethys.byu.edu/geoserver/rest/","tot_grace",'admin','geoserver')

    # Surface Water Storage Data
    # create_global_tiff_highres("/media/root/tethys/wmo_tethys-app/GRACE/tethysapp/grace/workspaces/app_workspace/gracedata/sw_/GRC_SW.nc","/Users/travismcstraw/tethysapps/GRACE/tethysapp/grace/workspaces/app_workspace/gracedata/sw_/global/geotiff_global/","lwe_thickness")
    # upload_global_tiff("/Users/travismcstraw/tethysapps/GRACE/tethysapp/grace/workspaces/app_workspace/gracedata/sw_/global/geotiff_global/","https://tethys.byu.edu/geoserver/rest/","sw_global",'admin','geoserver')
    # print('sw uploaded')

    # Soil Moisture Water Storage Data
    # create_global_tiff_highres("/media/root/tethys/wmo_tethys-app/GRACE/tethysapp/grace/workspaces/app_workspace/gracedata/soil_/GRC_Soil_Moisture_Total_Anomaly.nc","/Users/travismcstraw/tethysapps/GRACE/tethysapp/grace/workspaces/app_workspace/gracedata/soil_/global/geotiff_global/","lwe_thickness")
    # upload_global_tiff("/Users/travismcstraw/tethysapps/GRACE/tethysapp/grace/workspaces/app_workspace/gracedata/soil_/global/geotiff_global/","https://tethys.byu.edu/geoserver/rest/","soil_global",'admin','geoserver')
    # print('soil uploaded')

    # Groundwater Storage Data
    # create_global_tiff_highres("/media/root/tethys/wmo_tethys-app/GRACE/tethysapp/grace/workspaces/app_workspace/gracedata/gw_/GRC_gwtest.nc","/Users/travismcstraw/tethysapps/GRACE/tethysapp/grace/workspaces/app_workspace/gracedata/gw_/global/geotiff_global/","lwe_thickness")
    # upload_global_tiff("/Users/travismcstraw/tethysapps/GRACE/tethysapp/grace/workspaces/app_workspace/gracedata/gw_/global/geotiff_global/","https://tethys.byu.edu/geoserver/rest/","gw_global",'admin','geoserver')
    # print('gw uploaded')
    #-------------------------------------------------------------------------------------


    # Check for workspaces and create workspaces for app if they don't exist.
    # NOTE you will still need to enable wms service for these workspaces on the geoserver site.

    #-------------------------------------------------------------------------------------

    # Retrieve a geoserver engine
    geoserver_engine = app.get_spatial_dataset_service(name='main_geoserver', as_engine=True)


#     response = geoserver_engine.list_workspaces()

#     if response['success']:
#         workspaces = response['result']

#         if 'tot_global' not in workspaces:
#             geoserver_engine.create_workspace(workspace_id=tot_global, uri=www.googletot.com)
#         if 'sw_global' not in workspaces:
#             geoserver_engine.create_workspace(workspace_id=sw_global, uri=www.googlesw.com)
#         if 'soil_global' not in workspaces:
#             geoserver_engine.create_workspace(workspace_id=soil_global, uri=www.googlesoil.com)
#         if 'gw_global' not in workspaces:
#             geoserver_engine.create_workspace(workspace_id=gw_global, uri=www.googlegw.com)
#         if 'tot_grace' not in workspaces:
#             geoserver_engine.create_workspace(workspace_id=tot_grace, uri=www.googletotreg.com)
#         if 'sw_grace' not in workspaces:
#             geoserver_engine.create_workspace(workspace_id=sw_grace, uri=www.googleswreg.com)
#         if 'soil_grace' not in workspaces:
#             geoserver_engine.create_workspace(workspace_id=soil_grace, uri=www.googlesoilreg.com)
#         if 'gw_grace' not in workspaces:
#             geoserver_engine.create_workspace(workspace_id=gw_grace, uri=www.googlegwreg.com)
    #-------------------------------------------------------------------------------------


    Session = Grace.get_persistent_store_database('main_db',as_sessionmaker=True)
    session = Session()
    # Query DB for regions
    regions = session.query(Region).all()
    region_list = []

    for region in regions:
        region_list.append(("%s" % (region.display_name), region.id))

    session.close()
    if region_list:
        region_select = SelectInput(display_text='Select a Region',
                                    name='region-select',
                                    options=region_list, )
    else:
        region_select = None

    context = {
        "region_select": region_select, "regions_length": len(region_list), 'host': 'http://%s' % request.get_host()
    }

    return render(request, 'grace/home.html', context)


def api(request):

    context = {'host': 'http://%s' % request.get_host()}

    return render(request, 'grace/api.html', context)




def map(request):

    context = {}

    info = request.GET

    region_id = info.get('region-select')
    Session = Grace.get_persistent_store_database('main_db', as_sessionmaker=True)
    session = Session()

    region = session.query(Region).get(region_id)
    display_name = region.display_name

    bbox = [float(x) for x in region.latlon_bbox.strip("(").strip(")").split(',')]
    json.dumps(bbox)

    geoserver = session.query(Geoserver).get(region.geoserver_id)
    geoserver_url = geoserver.url
    region_store = ''.join(display_name.split()).lower()


    select_storage_type = SelectInput(display_text='Select Storage Component',
                                    name = 'select_storage_type',
                                    multiple=False,
                                    options= [('Total Water Storage (GRACE)', "tot"), ('Surface Water Storage (GLDAS)', "sw"), ('Soil Moisture Storage (GLDAS)', "soil"), ('Groundwater Storage (Calculated)', "gw")],
                                    initial=['']
                                    )

    FILE_DIR = os.path.join(TOTAL_NETCDF_DIR,'')

    region_dir = os.path.join(FILE_DIR+region_store,'')

    geotiff_dir = os.path.join(region_dir+"geotiff")

    sorted_files = sorted(os.listdir(geotiff_dir), key=lambda x: datetime.strptime(x, '%Y_%m_%d.tif'))
    layers_length = len(sorted_files)
    grace_layer_options = []

    for file in sorted_files:
        year = int(file[:-4].split('_')[0])
        month = int(file[:-4].split('_')[1])
        day = int(file[:-4].split('_')[2])
        date_str = datetime(year,month,day)
        date_str = date_str.strftime("%Y %B %d")
        grace_layer_options.append([date_str,file[:-4]+"_"+region_store])

    select_layer = SelectInput(display_text='Select a day',
                               name='select_layer',
                               multiple=False,
                               options=grace_layer_options, )

    csv_file = region_dir+region_store+".csv"
    with open(csv_file, 'rb') as f:
        reader = csv.reader(f)
        csvlist = list(reader)

    volume_time_series = []
    volume = []
    x_tracker = []
    formatter_string = "%m/%d/%Y"
    for item in csvlist:
        mydate = datetime.strptime(item[0], formatter_string)
        mydate = time.mktime(mydate.timetuple()) * 1000
        volume_time_series.append([mydate, float(item[1])])
        volume.append(float(item[1]))
        x_tracker.append(mydate)

    range = [round(min(volume), 2), round(max(volume), 2)]
    range = json.dumps(range)

    # Configure the time series Plot View
    # grace_plot = TimeSeries(
    #     engine='highcharts',
    #     title=display_name+ ' GRACE Data',
    #     y_axis_title='Total Terrestrial Water Storage Anomaly',
    #     y_axis_units='cm',
    #     series=[
    #         {
    #             'name': 'Height of Liquid Water',
    #             'color': '#0066ff',
    #             'data': volume_time_series,
    #         },
    #         {
    #             'name': 'Tracker',
    #             'color': '#ff0000',
    #             'data': [[min(x_tracker), round(min(volume), 2)], [min(x_tracker), round(max(volume), 2)]]
    #         },
    #     ],
    #     width='100%',
    #     height='300px'
    # )

    wms_url = geoserver_url[:-5]+"wms"
    color_bar = get_color_bar()
    color_bar = json.dumps(color_bar)

    if bbox[0] < 0 and bbox[2] < 0:
        map_center = [( (360+(int(bbox[0])))+(360+(int(bbox[2])))) / 2,(int(bbox[1])+int(bbox[3])) / 2]
    else:
        map_center = [(int(bbox[0]) + int(bbox[2])) / 2, (int(bbox[1]) + int(bbox[3])) / 2]
    json.dumps(map_center)
    json.dumps(x_tracker)

    context = {"region_id":region_id,"display_name":display_name,"wms_url":wms_url,"select_storage_type":select_storage_type,"select_layer":select_layer,"layers_length":layers_length,
               'x_tracker':x_tracker,"color_bar":color_bar,"range":range,"bbox":bbox,"map_center":map_center}

    return render(request, 'grace/map.html', context)

def global_map(request):

    color_bar = get_color_bar()
    color_bar = json.dumps(color_bar)

    grace_layer_options = get_global_dates(TOTAL_GLOBAL_NETCDF_DIR)

    slider_max = len(grace_layer_options)


    select_storage_type = SelectInput(display_text='Select Storage Component',
                                    name = 'select_storage_type',
                                    multiple=False,
                                    options= [('Total Water Storage (GRACE)', "tot"), ('Surface Water Storage (GLDAS)', "sw"), ('Soil Moisture Storage (GLDAS)', "soil"), ('Groundwater Storage (GRACE)', "gw")],
                                    initial=['']
                                    )

    select_layer = SelectInput(display_text='Select a day',
                               name='select_layer',
                               multiple=False,
                               options=grace_layer_options, )



    context = {'select_layer':select_layer,"select_storage_type":select_storage_type,'slider_max':slider_max,"color_bar":color_bar}

    return render(request, 'grace/global_map.html', context)



#@user_passes_test(user_permission_test)
def add_region(request):

    region_name_input = TextInput(display_text='Region Display Name',
                                     name='region-name-input',
                                     placeholder='e.g.: Utah',
                                     icon_append='glyphicon glyphicon-home',
                                     ) #Input for the Region Display Name

    Session = Grace.get_persistent_store_database('main_db', as_sessionmaker=True)
    session = Session()
    # Query DB for geoservers
    geoservers = session.query(Geoserver).all()
    geoserver_list = []
    for geoserver in geoservers:
        geoserver_list.append(( "%s (%s)" % (geoserver.name, geoserver.url),
                               geoserver.id))

    session.close()
    if geoserver_list:
        geoserver_select = SelectInput(display_text='Select a Geoserver',
                                       name='geoserver-select',
                                       options=geoserver_list,)
    else:
        geoserver_select = None

    add_button = Button(display_text='Add Region',
                        icon='glyphicon glyphicon-plus',
                        style='success',
                        name='submit-add-region',
                        attributes={'id': 'submit-add-region'}, )  # Add region button

    context = {"region_name_input":region_name_input, "geoserver_select": geoserver_select,"add_button":add_button}
    return render(request, 'grace/add_region.html', context)

#@user_passes_test(user_permission_test)
def add_geoserver(request):
    """
        Controller for the app add_geoserver page.
    """

    geoserver_name_input = TextInput(display_text='Geoserver Name',
                                     name='geoserver-name-input',
                                     placeholder='e.g.: BYU Geoserver',
                                     icon_append='glyphicon glyphicon-tag', )

    geoserver_url_input = TextInput(display_text='Geoserver REST Url',
                                    name='geoserver-url-input',
                                    placeholder='e.g.: http://tethys.byu.edu:8181/geoserver/rest',
                                    icon_append='glyphicon glyphicon-cloud-download')

    geoserver_username_input = TextInput(display_text='Geoserver Username',
                                         name='geoserver-username-input',
                                         placeholder='e.g.: admin',
                                         icon_append='glyphicon glyphicon-user', )

    add_button = Button(display_text='Add Geoserver',
                        icon='glyphicon glyphicon-plus',
                        style='success',
                        name='submit-add-geoserver',
                        attributes={'id': 'submit-add-geoserver'}, )

    context = {
        'geoserver_name_input': geoserver_name_input,
        'geoserver_url_input': geoserver_url_input,
        'geoserver_username_input': geoserver_username_input,
        'add_button': add_button,
    }

    return render(request, 'grace/add_geoserver.html', context)

#@user_passes_test(user_permission_test)
def manage_regions(request):
    """
    Controller for the app manage_geoservers page.
    """
    #initialize session
    Session = Grace.get_persistent_store_database('main_db', as_sessionmaker=True)
    session = Session()
    num_regions = session.query(Region).count()

    session.close()

    context = {
                'initial_page': 0,
                'num_regions': num_regions,
              }

    return render(request, 'grace/manage_regions.html', context)

#@user_passes_test(user_permission_test)
def manage_regions_table(request):
    """
    Controller for the app manage_geoservers page.
    """
    #initialize session
    Session = Grace.get_persistent_store_database('main_db', as_sessionmaker=True)
    session = Session()
    RESULTS_PER_PAGE = 5
    page = int(request.GET.get('page'))

    # Query DB for data store types
    regions = session.query(Region)\
                        .order_by(Region.display_name) \
                        .all()[(page * RESULTS_PER_PAGE):((page + 1)*RESULTS_PER_PAGE)]

    prev_button = Button(display_text='Previous',
                         name='prev_button',
                         attributes={'class':'nav_button'},)

    next_button = Button(display_text='Next',
                         name='next_button',
                         attributes={'class':'nav_button'},)

    context = {
                'prev_button' : prev_button,
                'next_button': next_button,
                'regions': regions,
              }

    session.close()

    return render(request, 'grace/manage_regions_table.html', context)
#@user_passes_test(user_permission_test)
def manage_geoservers(request):
    """
    Controller for the app manage_geoservers page.
    """
    #initialize session
    Session = Grace.get_persistent_store_database('main_db', as_sessionmaker=True)
    session = Session()
    num_geoservers = session.query(Geoserver).count()
    session.close()

    context = {
                'initial_page': 0,
                'num_geoservers': num_geoservers,
              }

    return render(request, 'grace/manage_geoservers.html', context)

#@user_passes_test(user_permission_test)
def manage_geoservers_table(request):
    """
    Controller for the app manage_geoservers page.
    """
    #initialize session
    Session = Grace.get_persistent_store_database('main_db', as_sessionmaker=True)
    session = Session()
    RESULTS_PER_PAGE = 5
    page = int(request.GET.get('page'))

    # Query DB for data store types
    geoservers = session.query(Geoserver)\
                        .order_by(Geoserver.name, Geoserver.url) \
                        .all()[(page * RESULTS_PER_PAGE):((page + 1)*RESULTS_PER_PAGE)]

    prev_button = Button(display_text='Previous',
                         name='prev_button',
                         attributes={'class':'nav_button'},)

    next_button = Button(display_text='Next',
                         name='next_button',
                         attributes={'class':'nav_button'},)

    context = {
                'prev_button' : prev_button,
                'next_button': next_button,
                'geoservers': geoservers,
              }

    session.close()

    return render(request, 'grace/manage_geoservers_table.html', context)



