class TableWidgetContent:
    # Услуги
    ServicesHist = ["sh_id", "sh_client", "sh_datetime", "sh_service", "sh_cost"]
    # Встречи
    Meetings = ["met_id", "met_datetime", "met_name", "met_status", "met_desc"]
    # Договоры
    Agreements = ["agr_id", "agr_deal", "agr_saler", "agr_buyer", "agr_status"]
    # Сделки
    Deals = ["deal_id", "deal_date", "deal_name", "deal_type", "deal_object",
             "deal_price", "deal_cpercent", "deal_csum", "deal_client", "deal_status"]

    Deals_c = ["deal_id", "deal_date", "deal_name", "deal_type", "deal_object",
             "deal_price", "deal_cpercent", "deal_csum", "deal_buyer", "deal_status"]
    # Клиенты
    Clients = ["cl_id", "cl_lname", "cl_fname", "cl_patronymic", "cl_passport", "cl_phone", "cl_email", "cl_address"]
    # Запросы
    Requests = ['req_id', 'req_client', 'req_details']
    # Объекты
    Objects = ["obj_id", "obj_name", "obj_owner", "obj_representative", "obj_second", "obj_type",
         "obj_dtype", "obj_square", "obj_rooms", "obj_price", "obj_address", "obj_desc", "obj_addpr"]

    # Представители
    Representatives = ["rep_id", "rep_name", "rep_phone", "rep_email", "rep_website", "rep_telegram", "rep_vk"]
    # Объекты клиентов
    ObjectsC = ["obj_id", "obj_cadastral", "obj_owner", "obj_name", "obj_type", "obj_square",
                "obj_rooms", "obj_price", "obj_adddate", "obj_target", "obj_status", "obj_address", "obj_desc", "obj_addprop"]
    # Гости
    Guests = ["gue_id", "gue_fullname", "gue_added", "gue_phone", "gue_blacklist"]
    # Показы
    Impressions = ["imp_id", "imp_datetime", "imp_object", "imp_guest", "imp_finished"]

    Object_addproperties = ["objp_id", "objp_bathrooms", "objp_floor", "objp_balcony", "objp_landplot",
                            "objp_garage", "objp_ldsquare", "objp_parking", "objp_yearbuilt",
                            "objp_basement", "objp_lastupd", "objp_kitchen_square", "objp_garbagech",
                            "objp_btype", "objp_cheight", "objp_accidentrate", "objp_repair"]

