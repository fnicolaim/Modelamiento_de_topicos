#Lista diccionarios
# l_dics

#Listas bautizos
l_bolsas_lema_stem = ['bols','compr','ilimit','consum','bolsa_mb','servici']
l_voz_lema_stem = ['problem','llam','comun','client','senal','cobertur','indic','hac','region']
l_recargas_lema_stem = ['recarg', 'sald', 'pes', 'lleg', 'client', 'verific', 'mont', 'medi']
l_solicitudes_lema_stem = ['client', 'realiz', 'llam', 'sald', 'plan', 'consult', 'solicit', 'lin', 'no_pod', 'recarg', 'indic']
l_canales_lema_stem = ["ingres","client","app","lug","acced","portal","aparec","registr","movil","mensaje_error"]
l_datos_lema_stem = ["naveg","si","equip","no_naveg","bols","client","cobertur","red","rrss","bam"]

l_gral_lema_stem_v6 = [("Bolsas",l_bolsas_lema_stem),("Voz",l_voz_lema_stem),("Recargas",l_recargas_lema_stem),("Solicitudes",l_solicitudes_lema_stem),("Canales",l_canales_lema_stem),("Datos",l_datos_lema_stem)]
l_gral_dic6 = dict(l_gral_lema_stem_v6)


voz2 = ["client","llam","lin","sald","ingres","realiz","indic","plan","consult","verific"]
datos2 = ["naveg", "comun","si","problem","cobertur","bols","senal","region","client","llam"]
otros2 = ["client","fech","app","compr","entreg","realiz","llam","punt","solicit","dificult"]
bolsas_recargas2 = ["bols","recarg","sald","pes","client","compr","verific","mont","consum", "ilimit"]

l_gral_lema_stem_v4 = [("Bolsas y recargas",bolsas_recargas2),("Voz",voz2),("Otros",otros2),("Datos",datos2)]
l_gral_dic4 = dict(l_gral_lema_stem_v4)

l_dics = [l_gral_dic4, l_gral_dic6]

#Diccionario de Diccionarios
D_d_D = {4 : l_gral_dic4 , 6: l_gral_dic6}