import	glob
import	os
from	django.conf			import settings
from	.objects.DataStorage	import DataStorage

def	is_file(name):
	try:
		file = open(name)
		return	(True)
	except:
		return	(False)

def	setSlot(slots, i, string):
	_tmp = slots[i]
	_tmp["status"] = string
	slots[i] = _tmp

def	save_elem(listFind, listRes, str):
	for _idx in listFind:
		if _idx.find(str) != -1:
			listRes.append(_idx)
			break

def	getFileName():
	_lst = glob.glob(settings.SAVED_PATH+"*.mmg")
	_num = 0
	while _num < len(_lst):
		_lst[_num] = _lst[_num].replace(settings.SAVED_PATH, "")
		_num += 1
	_rst = list()
	save_elem(_lst, _rst, "slota")
	save_elem(_lst, _rst, "slotb")
	save_elem(_lst, _rst, "slotc")
	_num = 0
	while _num < len(_rst):
		_rst[_num] = settings.SAVED_DIR + _rst[_num]
		print(_rst[_num])
		_num += 1
	return	_rst

def	ft_zero(slots, array):
	_num = 0
	_rst = [[-1, ""], [-1, ""], [-1, ""]]
	for _idx in array:
		if _rst[0][0] == -1:
			if (_idx[0].find("slota")) != -1:
				_rst[0] = [_num, _idx[0]]
		
		if _rst[1][0] == -1:
			if (_idx[0].find("slotb")) != -1:
				_rst[1] = [_num, _idx[0]]
		
		if _rst[2][0] == -1:
			if (_idx[0].find("slotc")) != -1:
				_rst[2] = [_num, _idx[0]]
		_num += 1
	if _rst[0][0] == -1:
		setSlot(slots, 0, "Free")
	if _rst[1][0] == -1:
		setSlot(slots, 1, "Free")
	if _rst[2][0] == -1:
		setSlot(slots, 2, "Free")
	return	_rst

def	ft_progress(slots, _rst, dic):
	_stm = " Moviemons"
	if _rst[0][0] != -1:
		_dic = dic.load(_rst[0][1])
		status = str(len(_dic.get("listMovieId"))) + "/" + str(settings.SIZE_MOVIE) + _stm
		setSlot(slots, 0, status)
	if _rst[1][0] != -1:
		_dic = dic.load(_rst[1][1])
		status = str(len(_dic.get("listMovieId"))) + "/" + str(settings.SIZE_MOVIE) + _stm
		setSlot(slots, 1, status)
	if _rst[2][0] != -1:
		_dic = dic.load(_rst[2][1])
		status = str(len(_dic.get("listMovieId"))) + "/" + str(settings.SIZE_MOVIE) + _stm
		setSlot(slots, 2, status)

def	init_slot(listParam):
	_nam = getFileName()
	_arr = list()
	for _idx in _nam:
		_arr.append([_idx, is_file(_idx)])
	_slt = listParam.get("slots")
	_dts = DataStorage()
	_dts.load_default_settings()
	_rst = ft_zero(_slt, _arr)
	ft_progress(_slt, _rst, _dts)
	return	_rst

def	changeData(listParam, arrayPath):
	_dts = DataStorage()
	if settings.INDEX == 0:
		_tmp = _dts.load(arrayPath[0][1])
	if settings.INDEX == 1:
		_tmp = _dts.load(arrayPath[1][1])
	if settings.INDEX == 2:
		_tmp = _dts.load(arrayPath[2][1])
	_dts.setPositionPlayer(_tmp["positionPlayer"])
	_dts.setAmountMovieBall(_tmp["amountMovieBall"])
	_dts.setListMovieName(_tmp["listMovieId"])
	_dts.setDataMovieIMDB(_tmp["dataMovieIMDB"])
	_dts.setMenuItem(_tmp["menuItem"])
	_dts.dump()
	return	True

def	changeText(buttons, rst, slot):
	if rst == "Free":
		return	False
	buttons['a'] = {"text" : "Start Game"}
	return	True

def	load_progress(listParam, arrayPath):
	_tmp = False
	_slt = listParam.get("slots")
	_btn = listParam.get("buttons")
	if settings.INDEX == 0:
		_rst = _slt[0].get("status")
		_tmp = changeText(_btn, _rst, 0)
	elif settings.INDEX == 1:
		_rst = _slt[1].get("status")
		_tmp = changeText(_btn, _rst, 1)
	elif settings.INDEX == 2:
		_rst = _slt[2].get("status")
		_tmp = changeText(_btn, _rst, 2)
	if _tmp == True:
		changeData(listParam, arrayPath)
		return	True
	return	False

def	save_game_file(arrayPath):
	_dts = DataStorage()
	try:
		_dic = _dts.load()
	except FileNotFoundError:
		_dts.load_default_settings()
		_dts.dump()
		_dic = _dts.load()
	if settings.INDEX == 0:
		_nam = "slota"
		if arrayPath[0][0] != -1:
			os.remove(arrayPath[0][1])
	elif settings.INDEX == 1:
		_nam = "slotb"
		if arrayPath[1][0] != -1:
			os.remove(arrayPath[1][1])
	elif settings.INDEX == 2:
		_nam = "slotc"
		if arrayPath[2][0] != -1:
			os.remove(arrayPath[2][1])
	_nam = settings.SAVED_DIR + _nam + "_" + \
		str(len(_dic.get("listMovieId"))) + "_" + \
		str(settings.SIZE_MOVIE) + ".mmg"
	_dts.setPositionPlayer(_dic["positionPlayer"])
	_dts.setAmountMovieBall(_dic["amountMovieBall"])
	_dts.setListMovieName(_dic["listMovieId"])
	_dts.setDataMovieIMDB(_dic["dataMovieIMDB"])
	_dts.setMenuItem(_dic["menuItem"])
	#_dts.dump(_nam)
