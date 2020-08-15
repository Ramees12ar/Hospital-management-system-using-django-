"""proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^$',home),
    url(r'^index',index,name="index"),                                  #home
    url(r'^hos_list',hos_list,name="hos_list"),                         #hospital list
    url(r'^patient_reg',patient_reg,name="patient_reg"),                #patient registration
    url(r'^login_ck',login_ck,name="login_ck"),                         #login check
    url(r'^hosp_reg',hosp_reg,name="hosp_reg"),                         #hospital registration
    url(r'^lab_reg',lab_reg,name="lab_reg"),                            #lab register
    url(r'^phar_reg',phar_reg,name="phar_reg"),                         #pharmacy register
    url(r'^login',login,name="login"),                                  #login portal redirect
    url(r'^phar',phar,name="phar"),                                     #pharmacy reg redirect
    url(r'^register',register,name="register"),                         #patient reg page redirect
    url(r'^hosp',hosp,name="hosp"),                                     #hospital reg page redirect
    url(r'^lab',lab,name="lab"),                                        #lab reg page redirect
    url(r'^main',main,name="main"),                                     #admin home page redirect
    url(r'^out',out,name="out"),                                        #logout redirect to home
    url(r'^adm_hosp',adm_hosp,name="adm_hosp"),                         #registering hospital to toc in admin portal
    url(r'^adm_phar',adm_phar,name="adm_phar"),                         #registering Pharmacy to toc in admin portal
    url(r'^adm_lab',adm_lab,name="adm_lab"),                            #registering labouratory to toc in admin portal
    url(r'^admin_hos',admin_hos,name="admin_hos"),                      #redirect to hospital page in admin portal when error registration occur
    url(r'^admin_lab',admin_lab,name="admin_lab"),                      #redirect to lab page in admin portal when error registration occur
    url(r'^admin_pha',admin_pha,name="admin_pha"),                      #redirect to pharmacy page in admin portal when error registration occur
    url(r'^app_hos',app_hos,name="app_hos"),                            #admin view of out hospital registration for approval
    url(r'^aprove_hos',aprove_hos,name="aprove_hos"),                   #admin approve the hospital and it stored in hosp regis and login db
    url(r'^app_lab',app_lab,name="app_lab"),                            #admin view of out lab registration for approval
    url(r'^aprove_lab',aprove_lab,name="aprove_lab"),                   #admin approve the lab and it stored in lab regis and login db
    url(r'^app_pha',app_pha,name="app_pha"),                            #admin view of out pharmacy registration for approval
    url(r'^aprove_pha',aprove_pha,name="aprove_pha"),                   #admin approve the pharmacy and it stored in phar regis and login db
    url(r'^ad_hosp_vw',ad_hosp_vw,name="ad_hosp_vw"),                   #admin view the registered hospitals
    url(r'^ad_lab_vw',ad_lab_vw,name="ad_lab_vw"),                      #admin view the registered outer labs and admin added labs
    url(r'^ad_pha_vw',ad_pha_vw,name="ad_pha_vw"),                      #admin view the registered outer phar and admin added phars
    url(r'^ad_pat_vw',ad_pat_vw,name="ad_pat_vw"),                      #admin view the registered patients
    url(r'^h_ad_delete',h_ad_delete,name="h_ad_delete"),                #delete hospital from the database
    url(r'^l_ad_delete',l_ad_delete,name="l_ad_delete"),                #delete lab from the database
    url(r'^p_ad_delete',p_ad_delete,name="p_ad_delete"),                #delete pharmacy from the database
    url(r'^refresh',refresh,name="refresh"),                            #refresh button used to update the status of data in admin page


    url(r'^hm_hosp',hm_hosp,name="hm_hosp"),                            #hospital home page
    url(r'^h_doc',h_doc,name="h_doc"),                                  #hospital portal redirect to adding doctor page
    url(r'^doc_h_add',doc_h_add,name="doc_h_add"),                      #adding doctors for the concern hospital
    url(r'^h_lab',h_lab,name="h_lab"),                                  #hospital portal redirect to adding lab page
    url(r'^ho_lab_add',ho_lab_add,name="ho_lab_add"),                   #adding labs for the concern hospital
    url(r'^h_pha',h_pha,name="h_pha"),                                  #hospital portal redirect to adding pharmacy page
    url(r'^pha_h_add',pha_h_add,name="pha_h_add"),                      #adding pharmacy for the concern hospital
    url(r'^hos_doc_vw',hos_doc_vw,name="hos_doc_vw"),                   #doctor list view for the hospital
    url(r'^del_h_doc',del_h_doc,name="del_h_doc"),                      #remove doc from hospital
    url(r'^hos_lab_vw',hos_lab_vw,name="hos_lab_vw"),                   #Lab list view for the hospital
    url(r'^del_h_lab',del_h_lab,name="del_h_lab"),                      #remove lab from hospital
    url(r'^hos_phar_vw',hos_phar_vw,name="hos_phar_vw"),                #Lab list view for the hospital
    url(r'^del_h_phar',del_h_phar,name="del_h_phar"),                   #remove lab from hospital
    url(r'^edit_hos',edit_hos,name="edit_hos"),                         #hospital profile edit
    url(r'^upd_hos',upd_hos,name="upd_hos"),                            #Hospital profile update
    url(r'^forget_pass',forget_pass,name="forget_pass"),                #password reset page
    url(r'reset',reset,name="reset"),                                   #reset password
    url(r'^fresh',fresh,name="fresh"),                                  #refresh in hospital
    url(r'^avail',avail,name="avail"),                                  #doctor available check
    


    url(r'^doct_hm',doct_hm,name="doct_hm"),                            #doctor hoem page
    url(r'^dr_bk_vw',dr_bk_vw,name="dr_bk_vw"),                         #Doctor book vw
    url(r'^qrcheck_dr',qrcheck_dr,name="qrcheck_dr"),                   #qr check and redirect
    url(r'^test_dr',test_dr,name="test_dr"),                            #add test
    url(r'^pre_dr',pre_dr,name="pre_dr"),                               #prescription
    url(r'^back',back,name="back"),                                     #redirect to qr view page
    url(r'^submit',submit,name="submit"),                               #consultaion

    
    url(r'^pat_hm',pat_hm,name="pat_hm"),                               #Patient home
    url(r'^for_log',for_log,name="for_log"),                            #login page for patient
    url(r'^check_log',check_log,name="check_log"),                      #patient login for book appointment from home
    url(r'^pt_hm_book',pt_hm_book,name="pt_hm_book"),                   #book appointment from patient page
    url(r'^vw_dr',vw_dr,name="vw_dr"),                                  #doctor booking view patient portal
    url(r'^pt_test',pt_test,name="pt_test"),                            #lab history
    url(r'^pt_pre',pt_pre,name="pt_pre"),                               #prescription history
    
    url(r'^homelab',homelab,name="homelab"),                            #labouratory homea page
    url(r'^tst_lab',tst_lab,name="tst_lab"),                            #lab qrcode check after
    url(r'^lstatus',lstatus,name="lstatus"),                            #lab test complete
    url(r'^vow_lab',vow_lab,name="vow_lab"),                            #lab test view request
    url(r'^info',info,name="info"),                                     #upload page
    url(r'^file_lab',file_lab,name="file_lab"),                         #upload file


    url(r'^o_labo_hm',o_labo_hm,name="o_labo_hm"),                      #out lab home page
    url(r'^ot_tst_lab',ot_tst_lab,name="ot_tst_lab"),                   #lab qrcode check after
    url(r'^aout_info',aout_info,name="aout_info"),                      #upload page
    url(r'^bout_file_lab',bout_file_lab,name="bout_file_lab"),          #upload file
    


    url(r'^pha_hm',pha_hm,name="pha_hm"),                               #pharmacy homea page
    url(r'^presc_pha',presc_pha,name="presc_pha"),                      #Pharmacy qrcode check after
    url(r'^pstatus',pstatus,name="pstatus"),                            #after medicine given
    url(r'^vew_presc',vew_presc,name="vew_presc"),                      #hosp pharamacy view
    url(r'^me_vw',me_vw,name="me_vw"),                                  #stock medicine view
    url(r'^pg_med_add',pg_med_add,name="pg_med_add"),                    #Add med pag
    url(r'^stock',stock,name="stock"),                                   #add medicine
    url(r'^print_bill',print_bill,name="print_bill"),                   #print bill



    url(r'^aa_o_pha_hm',aa_o_pha_hm,name="aa_o_pha_hm"),                #out pharmacy home page
    url(r'^kout_presc_pha',kout_presc_pha,name="kout_presc_pha"),       #out phar qrcode after
    url(r'^mout_pstatus',mout_pstatus,name="mout_pstatus"),             #after medicine given
    url(r'^vv_med_add',vv_med_add,name="vv_med_add"),                   #add medicine
    url(r'^yy_stock',yy_stock,name="yy_stock"),                         #update stock
    url(r'^ee_vw',ee_vw,name="ee_vw"),                                  #stock medicine view
    
    
    url(r'^list_hosp',list_hosp,name="list_hosp"),                      #hospital list
    url(r'^list_dept',list_dept,name="list_dept"),                      #hospital department
    url(r'^list_dr',list_dr,name="list_dr"),                            #hospital doctor
    url(r'^book_now',book_now,name="book_now"),                         #appointemnet doctor
    url(r'^stk_med',stk_med,name="stk_med"),                            #medicine stock check
    url(r'^z_stock',z_stock,name="z_stock"),                            #stock checker
    url(r'^autocomplete',autocomplete,name="autocomplete"),             #auto medicine load
    url(r'^medchecker',medchecker,name="medchecker"),                   #medicine availability checker

    url(r'^appoit',appoit,name="appoit"),                               #add appointmnet
    url(r'^recp',recp,name="recp"),                                     #add reception
    url(r'^wdept',wdept,name="wdept"),                                  #hosp departmenst
    url(r'^pbooking',pbooking,name="pbooking"),
    url(r'^iibook',iibook,name="iibook"),
    url(r'nn_list_dr',nn_list_dr,name="nn_list_dr"),
    
   #url(r'^patient_reg',patient_reg,name="Patient"),
   # url(r'^doc_reg',doc_reg,name="Doctor"),
   # url(r'^hosp_reg',hosp_reg,name="Hospital"),
   # url(r'^phar_reg',phar_reg,name="Pharmacy"),
   # url(r'^lab_reg',lab_reg,name="Labouratory"),
   # url(r'^o_hosp_reg',o_hosp_reg,name="Hospital"),
   # url(r'^o_phar_reg',o_phar_reg,name="Pharmacy"),
   # url(r'^o_lab_reg',o_lab_reg,name="Labouratory"),    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
