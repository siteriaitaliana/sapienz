# https://sites.google.com/a/chromium.org/chromedriver/downloads

# Copyright (c) 2016-present, Ke Mao. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
#     * The names of the contributors may not be used to endorse or
#       promote products derived from this software without specific
#       prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import random
import os
import sys
import pickle
import datetime
import subprocess
import platform
import numpy
from deap import creator, base, tools
from algorithms import eaMuPlusLambdaParallel
from reproRunner import reproRunner
import settings
# from coverages import emma_coverage
# from coverages import ella_coverage
# from coverages import act_coverage
from plot import two_d_line
# from devices import emulator
# from crashes import crash_handler
from analysers import static_analyser
from init import initRepeatParallel


class CanNotInitSeqException(Exception):
	pass

# get one test suite by running multiple times of MotifCore
# def get_suite():
# 	ret = []
# 	# unique_crashes = set()
# 	# for i in range(0, settings.SUITE_SIZE):
# 	# 	# get_sequence may return empty sequence
# 	# 	seq = []
# 	# 	repeated = 0
# 	# 	while len(seq) <= 2:
# 	# 		seq = get_sequence(i, unique_crashes)
# 	# 		repeated += 1
# 	# 		if repeated > 20:
# 	# 			raise CanNotInitSeqException("Cannot get sequence via MotifCore.")
# 	# 	ret.append(seq)

# 	return [
# 		["clicker mouseover at 892 602","clicker mouseout at 776 835","clicker dblclick at 573 547","clicker mouseover at 821 30","clicker click at 1235 206","clicker click at 1081 11","clicker mousedown at 120 861","clicker mouseout at 1653 280","clicker mouseover at 1559 277","clicker click at 1666 796","clicker mousemove at 81 1010","clicker click at 1294 26","clicker click at 1808 830","clicker mouseover at 432 570"],
# 		["clicker click at 686 586","clicker dblclick at 1672 28","clicker mouseover at 781 768","clicker click at 441 1068","clicker mouseover at 1167 610","clicker click at 411 334","clicker mousemove at 1002 1049","clicker click at 994 742","clicker mouseover at 405 737","clicker mouseup at 1888 472","clicker click at 1761 456","clicker click at 1498 347","clicker dblclick at 916 726","clicker click at 679 920","clicker mouseout at 1189 237","clicker mousedown at 1034 593"],
# 		["clicker dblclick at 1227 1064","clicker click at 39 896","clicker click at 1487 605","clicker mouseover at 1443 854","clicker click at 784 932","clicker mousemove at 1274 390","clicker mouseover at 281 789","clicker dblclick at 1154 158","clicker dblclick at 1009 565","clicker mousedown at 708 242","clicker mouseover at 1582 845","clicker mouseover at 232 433","clicker mouseout at 684 535","clicker click at 1557 667","clicker click at 1216 502","clicker click at 1405 668"]	
# 		]

### helper functions
# get one event sequence by running revised motifcore
# note: the luanch activity is started by emma instrument
# def get_sequence(index, unique_crashes):
	# std_out_file = apk_dir + "/intermediate/" + "output.stdout"
	# random.seed()

	# motifcore_events = random.randint(settings.SEQUENCE_LENGTH_MIN, settings.SEQUENCE_LENGTH_MAX)

	# ret = []

	# clear data
	# os.system("adb -s " + device + " shell pm clear " + package_name)

	# start motifcore
	# print ("... Start generating a sequence")
	# command = Command("adb -s " + device + " shell motifcore -p " + package_name + " -v --throttle " + str(
	# 	settings.THROTTLE) + " " + str(motifcore_events))
	# command.run(timeout=600)
	# cmd = "adb -s " + device + " shell motifcore -p " + package_name + " --ignore-crashes --ignore-security-exceptions --ignore-timeouts --bugreport --string-seeding /mnt/sdcard/" + package_name + "_strings.xml -v " + str(
	# 	motifcore_events)
	# os.system(settings.TIMEOUT_CMD + " " + str(settings.EVAL_TIMEOUT) + " " + cmd)
	# # need to kill motifcore when timeout
	# kill_motifcore_cmd = "shell ps | awk '/com\.android\.commands\.motifcore/ { system(\"adb -s " + device + " shell kill \" $2) }'"
	# os.system("adb -s " + device + " " + kill_motifcore_cmd)

	# print ("... Finish generating a sequence")
	# access the generated script, should ignore the first launch activity
	# # script_name = settings.MOTIFCORE_SCRIPT_PATH.split("/")[-1]
	# # ts = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S.%f")[:-3]
	# # os.system(
	# # 	"adb -s " + device + " pull " + settings.MOTIFCORE_SCRIPT_PATH + " " + apk_dir + "/intermediate/" + script_name + ".init." + ts + "." + str(
	# # 		index))
	# # script = open(apk_dir + "/intermediate/" + script_name + ".init." + ts + "." + str(index))
	# # is_content = False
	# # is_skipped_first = False
	# for line in script:
	# 	line = line.strip()
	# 	if line.find("start data >>") != -1:
	# 		is_content = True
	# 		continue
	# 	if is_content and line != "":
	# 		if is_skipped_first == False:
	# 			is_skipped_first = True
	# 			continue
	# 		if is_skipped_first:
	# 			ret.append(line)

	# script.close()

	# deal with crash
	# crash_handler.handle(device, apk_dir, apk_dir + "/intermediate/" + script_name + ".init." + ts + "." + str(index),
	# 					 "init", ts, index, unique_crashes)

	# return ret


# generate individual by running motifcore
def gen_individual():
	# if settings.DEBUG:
	# 	print ("Generate Individual on device, ", device)
	suite = [
     		{"history_index": None, "crowding_dist": None, "fitness":  {"valid": False, "values": None}, "sequence": 
			["clicker click at 500 459","clicker mousedown at 346 642","clicker click at 885 1068","clicker click at 1407 770","clicker click at 922 617","clicker mouseover at 330 863","clicker dblclick at 552 1079","clicker mousedown at 120 596","clicker dblclick at 1505 722","clicker click at 360 141","clicker mouseover at 1422 884","clicker mousedown at 387 739","clicker click at 906 636","clicker dblclick at 767 170","clicker click at 1869 84","clicker click at 640 397","clicker mouseup at 1214 979","clicker dblclick at 89 1077","clicker mouseover at 374 808","clicker click at 460 82","clicker mouseup at 1910 472","clicker mousedown at 367 509","clicker mousemove at 19 612","clicker mouseout at 315 1053","clicker click at 235 787","clicker dblclick at 54 180","clicker mouseover at 1430 1058","clicker click at 1350 310","clicker mousedown at 1090 30","clicker mouseover at 759 418","clicker click at 928 65","clicker click at 1601 922","clicker mouseover at 908 896","clicker dblclick at 1856 167","clicker mouseover at 756 677","clicker mouseover at 1134 3","clicker click at 1449 663","clicker click at 1496 561","clicker click at 685 397","clicker mousemove at 387 17","clicker click at 1030 645","clicker dblclick at 1694 115","clicker mouseover at 1540 1007","clicker dblclick at 1333 443","clicker click at 1892 929","clicker click at 1399 764","clicker mouseout at 372 642","clicker dblclick at 491 516","clicker mouseover at 1740 244","clicker mouseover at 1820 58","clicker dblclick at 909 154","clicker dblclick at 938 565","clicker dblclick at 429 516","clicker click at 1877 1012","clicker click at 468 814","clicker click at 962 89","clicker click at 612 522","clicker dblclick at 659 812","clicker click at 50 222","clicker dblclick at 835 216","clicker click at 1313 998","clicker mouseover at 671 411","clicker dblclick at 1 208","clicker click at 376 300","clicker click at 84 264","clicker click at 4 691","clicker mouseover at 1784 447","clicker mouseup at 226 550","clicker click at 883 377","clicker mouseup at 390 947","clicker dblclick at 293 280","clicker mousedown at 839 178","clicker mouseover at 26 737","clicker dblclick at 1828 1067","clicker mouseup at 93 867","clicker click at 1436 362","clicker dblclick at 734 662","clicker mouseover at 297 287","clicker click at 17 542","clicker dblclick at 1005 1065","clicker mousemove at 1697 763","clicker mouseout at 1873 500","clicker mouseover at 1395 597","clicker click at 749 507","clicker mousedown at 1472 524","clicker mouseup at 438 317","clicker click at 610 338","clicker mouseout at 365 406","clicker click at 532 334","clicker click at 372 185","clicker mouseover at 391 888","clicker click at 215 1076","clicker mousemove at 1187 909","clicker mouseover at 918 668","clicker click at 552 1063","clicker mouseover at 308 514","clicker mouseup at 59 61","clicker mouseover at 627 408","clicker mouseover at 1277 326","clicker mousedown at 606 354","clicker click at 982 752","clicker mousemove at 120 287","clicker mouseover at 1760 1066","clicker click at 1712 1016","clicker mousemove at 859 814","clicker mouseover at 1584 851","clicker click at 1563 433","clicker click at 402 292","clicker click at 448 802","clicker mouseover at 1359 653","clicker mousemove at 422 441","clicker click at 1136 521","clicker click at 912 788","clicker mouseover at 1612 1066","clicker click at 840 702","clicker mouseout at 1508 374","clicker mouseover at 986 860","clicker dblclick at 669 322","clicker mouseup at 1461 1060","clicker mousemove at 1119 956","clicker click at 1013 854","clicker click at 1082 972","clicker mouseout at 1006 608","clicker click at 811 597","clicker mouseup at 1752 555","clicker mousemove at 206 1022","clicker click at 645 161","clicker click at 1323 449","clicker mouseup at 533 613","clicker dblclick at 1074 699","clicker dblclick at 1873 237","clicker dblclick at 328 303","clicker mouseup at 1653 900","clicker click at 1313 609","clicker mouseover at 1745 1029","clicker mousedown at 1353 640","clicker mouseover at 1722 51","clicker click at 363 835","clicker click at 1165 671","clicker mousedown at 679 38","clicker mouseover at 599 1044","clicker click at 356 756","clicker mouseover at 841 1037","clicker mousedown at 131 18","clicker click at 1553 58","clicker dblclick at 1528 910","clicker click at 1528 323","clicker click at 1320 196","clicker click at 669 668","clicker dblclick at 1177 327","clicker mousedown at 721 1023","clicker mouseover at 582 1051","clicker mouseout at 1456 724","clicker click at 1200 171","clicker mouseout at 1501 905","clicker mouseover at 1493 776","clicker click at 1699 96","clicker mousemove at 1864 700","clicker click at 602 525","clicker mouseover at 924 24","clicker mouseover at 62 696","clicker click at 575 635","clicker mouseover at 161 477","clicker click at 1828 1061","clicker mousedown at 473 906","clicker click at 1399 434","clicker click at 413 590","clicker mouseover at 1697 572","clicker dblclick at 158 341","clicker mouseout at 839 894","clicker dblclick at 1040 831","clicker click at 1169 365","clicker mouseover at 1575 982","clicker mouseover at 401 689","clicker click at 1497 457","clicker mouseover at 1564 382","clicker mouseover at 519 335","clicker mousedown at 818 420","clicker click at 1631 331","clicker click at 1859 693","clicker click at 985 306","clicker click at 1593 505","clicker mouseover at 173 1042","clicker mouseup at 1068 541","clicker dblclick at 1218 82","clicker click at 566 794","clicker mousemove at 1321 521","clicker click at 3 0","clicker dblclick at 561 24","clicker mouseup at 379 359","clicker click at 1140 523","clicker click at 471 485","clicker click at 860 595","clicker click at 1486 764","clicker mouseover at 1745 902","clicker dblclick at 342 158","clicker click at 135 504","clicker mousemove at 152 283","clicker mouseup at 1788 284","clicker click at 1652 133","clicker click at 1178 427","clicker mousedown at 531 647","clicker mouseout at 1359 360","clicker click at 1467 404","clicker mouseup at 883 605","clicker dblclick at 1742 588","clicker mousemove at 806 268","clicker click at 1789 359","clicker mouseout at 1845 121","clicker mouseout at 719 896","clicker mouseover at 1500 189","clicker click at 1633 1046","clicker mousedown at 1044 373","clicker click at 1259 907","clicker click at 110 702","clicker click at 1048 643","clicker dblclick at 463 939","clicker mouseover at 1354 904","clicker mouseover at 635 976","clicker mouseover at 1816 210","clicker dblclick at 117 657","clicker mouseover at 1653 1074","clicker dblclick at 381 148","clicker mouseup at 1321 675","clicker click at 359 470","clicker click at 530 500","clicker dblclick at 1236 916","clicker click at 65 866","clicker mousedown at 1761 325","clicker mousedown at 505 685","clicker click at 1280 28","clicker mousedown at 892 651","clicker click at 1559 288","clicker mousemove at 612 1054","clicker mousedown at 1338 515","clicker click at 426 198","clicker mouseover at 801 525","clicker click at 221 185","clicker click at 922 46","clicker mousedown at 203 143","clicker mouseover at 891 858","clicker click at 1878 820","clicker dblclick at 718 406","clicker click at 256 307","clicker click at 453 44","clicker mouseout at 1032 452","clicker click at 278 76","clicker mouseover at 1068 823","clicker mouseover at 376 557","clicker click at 1469 923","clicker mousedown at 463 746","clicker mouseover at 670 557","clicker click at 1359 880","clicker mousedown at 1375 72","clicker dblclick at 102 373","clicker mouseover at 1796 304","clicker mousedown at 58 957","clicker click at 1290 540","clicker mouseup at 1827 47","clicker click at 837 883","clicker mouseover at 1714 320","clicker mouseover at 442 521","clicker click at 732 613","clicker click at 1876 813","clicker click at 839 187","clicker click at 183 489","clicker mousemove at 816 1063","clicker mouseover at 729 313","clicker mouseover at 1759 308","clicker mouseover at 1186 523","clicker dblclick at 246 44","clicker click at 1761 962","clicker mouseover at 863 236","clicker click at 3 719","clicker dblclick at 698 247","clicker click at 1892 914","clicker click at 32 832","clicker mouseover at 831 859","clicker dblclick at 97 689","clicker mouseover at 1672 163","clicker mouseover at 83 169","clicker click at 1392 642","clicker mousemove at 2 584","clicker mouseout at 522 44","clicker dblclick at 1220 160","clicker click at 1479 20","clicker mousemove at 422 195","clicker mousedown at 1427 752","clicker mousedown at 179 889","clicker mouseup at 1039 566","clicker mouseup at 1180 525","clicker mouseover at 1004 879","clicker click at 238 888","clicker mousedown at 1646 150","clicker click at 164 867","clicker dblclick at 149 660","clicker mousedown at 1215 120","clicker click at 706 867","clicker click at 1898 987","clicker mouseup at 553 475","clicker dblclick at 1257 457","clicker mouseout at 1379 461","clicker click at 81 458","clicker click at 1293 685","clicker click at 266 1074","clicker mouseover at 10 648","clicker mouseover at 1557 679","clicker mouseover at 112 128","clicker mousemove at 1352 53","clicker mouseover at 428 957","clicker click at 128 1049","clicker mouseover at 25 631","clicker click at 1323 327","clicker dblclick at 1011 895","clicker click at 1064 324","clicker mouseover at 1845 1028","clicker click at 15 43","clicker mousedown at 477 336","clicker click at 1094 585","clicker mouseover at 126 638","clicker mouseover at 1399 1074","clicker click at 946 557","clicker mouseover at 1444 526","clicker dblclick at 939 28","clicker mouseout at 1834 610","clicker click at 81 551","clicker mouseup at 223 771","clicker click at 911 853","clicker click at 1167 1072","clicker mouseover at 1454 485","clicker dblclick at 439 919","clicker dblclick at 273 1075","clicker click at 123 202","clicker mouseout at 954 527","clicker mouseup at 1695 379","clicker mouseover at 548 625","clicker mouseout at 1911 662","clicker mouseover at 1192 105","clicker click at 625 596","clicker mouseover at 1612 878","clicker click at 355 620","clicker mousemove at 1306 140","clicker click at 103 42","clicker mousedown at 994 275","clicker dblclick at 1046 161","clicker mousedown at 775 380","clicker dblclick at 218 341","clicker mouseup at 1200 904","clicker mouseout at 1304 760","clicker mouseout at 1178 212","clicker dblclick at 1491 968","clicker click at 1705 842","clicker click at 926 729","clicker click at 275 270","clicker click at 558 299"]			}
       		,
 			{"history_index": None, "crowding_dist": None, "fitness":  {"valid": False, "values": None}, "sequence": 
			["clicker click at 686 586","clicker dblclick at 1672 28","clicker mouseover at 781 768","clicker click at 441 1068","clicker mouseover at 1167 610","clicker click at 411 334","clicker mousemove at 1002 1049","clicker click at 994 742","clicker mouseover at 405 737","clicker mouseup at 1888 472","clicker click at 1761 456","clicker click at 1498 347","clicker dblclick at 916 726","clicker click at 679 920","clicker mouseout at 1189 237","clicker mousedown at 1034 593","clicker click at 1891 151","clicker dblclick at 1861 935","clicker mouseover at 1513 635","clicker click at 1459 90","clicker click at 852 420","clicker mouseup at 745 959","clicker click at 147 638","clicker click at 1040 975","clicker mouseout at 616 554","clicker mouseout at 642 652","clicker click at 1210 935","clicker click at 1173 211","clicker dblclick at 856 809","clicker click at 1919 871","clicker mousedown at 1484 324","clicker click at 118 713","clicker mouseover at 1797 901","clicker mouseout at 408 816","clicker click at 536 621","clicker mousemove at 663 774","clicker click at 104 496","clicker mouseover at 1709 115","clicker mouseup at 76 912","clicker click at 351 1015","clicker click at 408 709","clicker click at 217 912","clicker mousedown at 924 624","clicker mouseup at 1301 539","clicker click at 1117 817","clicker dblclick at 25 599","clicker dblclick at 1421 726","clicker mouseover at 558 83","clicker click at 1746 534","clicker click at 1139 597","clicker click at 123 975","clicker click at 1384 822","clicker click at 1714 45","clicker mouseover at 1614 955","clicker click at 1500 852","clicker mousemove at 1829 419","clicker mouseup at 1305 87","clicker mouseout at 410 1023","clicker mousedown at 1054 512","clicker click at 958 193","clicker mouseover at 648 1070","clicker click at 254 805","clicker mouseover at 681 520","clicker mouseout at 488 506","clicker mousedown at 1135 178","clicker mousemove at 1481 287","clicker click at 1478 627","clicker mouseout at 1131 455","clicker click at 1453 857","clicker mouseover at 911 358","clicker click at 1261 446","clicker dblclick at 1190 612","clicker mouseover at 1725 542","clicker click at 496 85","clicker mouseover at 1874 27","clicker mouseover at 1254 724","clicker mousemove at 576 950","clicker mousemove at 239 780","clicker dblclick at 861 212","clicker click at 409 251","clicker mouseup at 975 821","clicker mouseover at 1735 21","clicker click at 373 16","clicker dblclick at 1011 917","clicker mousemove at 954 139","clicker mouseover at 662 175","clicker mouseup at 274 1078","clicker mouseover at 1489 19","clicker dblclick at 1274 965","clicker dblclick at 288 855","clicker mouseover at 1455 177","clicker dblclick at 1387 84","clicker click at 1858 150","clicker mouseover at 926 372","clicker mouseover at 1580 260","clicker click at 1243 1077","clicker dblclick at 44 789","clicker mousedown at 1760 965","clicker click at 629 896","clicker dblclick at 1032 474","clicker mouseup at 328 648","clicker click at 389 967","clicker click at 886 636","clicker click at 467 638","clicker dblclick at 1483 234","clicker mouseover at 1556 95","clicker click at 1418 618","clicker mouseover at 1026 772","clicker dblclick at 332 1063","clicker mouseover at 1751 551","clicker click at 1340 321","clicker dblclick at 1477 354","clicker mouseout at 207 1071","clicker mouseout at 43 472","clicker click at 1716 320","clicker dblclick at 378 90","clicker click at 250 890","clicker mouseup at 732 639","clicker mouseover at 1292 889","clicker click at 668 1071","clicker dblclick at 1611 676","clicker click at 1360 500","clicker mouseout at 1185 701","clicker mousemove at 900 645","clicker click at 449 981","clicker dblclick at 344 716","clicker mousemove at 642 994","clicker click at 1429 519","clicker dblclick at 778 325","clicker click at 1703 390","clicker mouseover at 1544 887","clicker mouseup at 601 873","clicker dblclick at 1603 772","clicker mousemove at 456 251","clicker click at 1221 417","clicker mouseover at 424 707","clicker mouseover at 994 295","clicker mouseover at 119 556","clicker click at 1521 1068","clicker mouseup at 228 517","clicker mouseup at 924 790","clicker mousemove at 841 472","clicker click at 168 582","clicker click at 1516 819","clicker dblclick at 1863 736","clicker dblclick at 1045 725","clicker click at 472 488","clicker dblclick at 1190 379","clicker click at 1645 649","clicker click at 1782 1009","clicker mousemove at 1130 84","clicker click at 456 970","clicker mousemove at 66 550","clicker mouseover at 942 28","clicker click at 486 146","clicker click at 291 598","clicker mouseover at 1421 156","clicker click at 407 478","clicker click at 479 395","clicker mouseover at 19 371","clicker mousemove at 747 855","clicker mouseover at 1449 962","clicker click at 1534 131","clicker click at 1013 559","clicker dblclick at 31 73","clicker mouseover at 1218 566","clicker mouseup at 270 894","clicker mousemove at 1173 848","clicker mousedown at 1915 130","clicker mouseup at 514 219","clicker mouseover at 1730 1052","clicker click at 1864 727","clicker click at 1141 141","clicker click at 487 436","clicker click at 1170 694","clicker click at 604 486","clicker click at 953 549","clicker mousemove at 1329 345","clicker click at 1588 874","clicker mousedown at 214 583","clicker mousemove at 180 289","clicker click at 1450 725","clicker click at 338 872","clicker mouseup at 614 347","clicker click at 1736 1039","clicker mouseover at 1359 525","clicker click at 1472 519","clicker mouseover at 1485 1037","clicker mouseover at 647 674","clicker click at 1395 618","clicker mousedown at 734 125","clicker mouseover at 673 751","clicker mouseover at 706 635","clicker mousedown at 1807 491","clicker click at 1456 657","clicker click at 1754 117","clicker click at 116 88","clicker dblclick at 708 1033","clicker click at 1119 938","clicker mouseout at 1727 183","clicker click at 1837 16","clicker dblclick at 1006 406","clicker mouseout at 1913 1033","clicker click at 1509 714","clicker click at 384 469","clicker click at 768 295","clicker dblclick at 304 1057","clicker mouseover at 1083 913","clicker mousemove at 1007 425","clicker dblclick at 1122 653","clicker mouseout at 922 118","clicker click at 1113 730","clicker dblclick at 1752 895","clicker mousedown at 1611 778","clicker click at 355 179","clicker mouseover at 1516 963","clicker mousedown at 1075 747","clicker mousedown at 1244 124","clicker mouseover at 60 727","clicker dblclick at 1830 283","clicker click at 414 874","clicker mouseup at 746 694","clicker mousemove at 637 749","clicker dblclick at 1292 153","clicker dblclick at 1242 633","clicker click at 954 705","clicker mouseup at 1536 980","clicker mousemove at 1469 946","clicker click at 589 176","clicker dblclick at 141 193","clicker mouseover at 1323 321","clicker mouseup at 948 351","clicker click at 1661 1053","clicker click at 1654 862","clicker dblclick at 1638 63","clicker dblclick at 744 76","clicker mouseup at 684 310","clicker click at 960 970","clicker click at 584 984","clicker mouseup at 1809 793","clicker dblclick at 1292 628","clicker mousedown at 1578 43","clicker mouseover at 1257 205","clicker click at 23 752","clicker click at 1811 931","clicker click at 1332 52","clicker mousemove at 1527 936","clicker dblclick at 1528 318","clicker click at 236 363","clicker dblclick at 1631 681","clicker mousedown at 572 237","clicker click at 962 5","clicker dblclick at 491 784","clicker dblclick at 203 233","clicker mouseover at 225 818","clicker click at 1498 1008","clicker mousemove at 121 762","clicker mouseover at 1707 55","clicker mousemove at 1011 316","clicker mouseover at 693 320","clicker mouseup at 1013 195","clicker click at 1886 230","clicker dblclick at 1388 870","clicker dblclick at 1791 868","clicker mouseup at 1375 508","clicker click at 692 442","clicker mouseover at 1381 1038","clicker click at 510 381","clicker dblclick at 1696 270","clicker mouseover at 1536 935","clicker mouseover at 224 4","clicker click at 1398 377","clicker click at 748 989","clicker click at 701 862","clicker click at 1712 524","clicker mouseover at 998 587","clicker click at 1900 661","clicker dblclick at 251 843","clicker click at 372 391","clicker mouseover at 886 825","clicker mousemove at 1002 864","clicker mousemove at 1582 447","clicker click at 284 952","clicker mousemove at 1675 1037","clicker click at 1161 141","clicker click at 65 922","clicker click at 392 223","clicker mouseout at 1407 797"]
			},
       		{"history_index": None, "crowding_dist": None, "fitness":  {"valid": False, "values": None}, "sequence": 
			['clicker dblclick at 1227 1064', 'clicker click at 286 853', 'clicker click at 784 932', 'clicker click at 1407 770', 'clicker click at 922 617', 'clicker mouseover at 330 863', 'clicker dblclick at 1009 565', 'clicker mouseover at 1506 840', 'clicker dblclick at 1505 722', 'clicker click at 360 141', 'clicker mouseover at 1422 884', 'clicker mousedown at 387 739', 'clicker click at 906 636', 'clicker dblclick at 767 170', 'clicker click at 1869 84', 'clicker click at 716 1027', 'clicker mouseup at 1214 979', 'clicker dblclick at 89 1077', 'clicker dblclick at 1919 238', 'clicker mouseout at 668 385', 'clicker mouseup at 1910 472', 'clicker click at 1216 483', 'clicker dblclick at 736 234', 'clicker mouseout at 315 1053', 'clicker mouseover at 1065 619', 'clicker click at 1622 629', 'clicker mouseover at 1430 1058', 'clicker mouseover at 1059 510', 'clicker mouseout at 1451 1009', 'clicker mouseover at 1228 531', 'clicker mouseout at 1410 758', 'clicker click at 1601 922', 'clicker click at 1714 410', 'clicker dblclick at 1856 167', 'clicker mouseover at 756 677', 'clicker mouseover at 1134 3', 'clicker click at 1449 663', 'clicker click at 1496 561', 'clicker click at 685 397', 'clicker click at 1181 868', 'clicker click at 493 371', 'clicker dblclick at 1694 115', 'clicker mousedown at 720 274', 'clicker dblclick at 379 184', 'clicker click at 1892 929', 'clicker click at 1399 764', 'clicker mouseup at 90 817', 'clicker click at 839 156', 'clicker click at 1308 601', 'clicker mouseover at 1820 58', 'clicker dblclick at 909 154', 'clicker dblclick at 938 565', 'clicker mousemove at 1818 917', 'clicker click at 1877 1012', 'clicker mouseover at 368 2', 'clicker click at 1632 69', 'clicker click at 206 303', 'clicker mouseover at 1167 800', 'clicker click at 50 222', 'clicker dblclick at 835 216', 'clicker mousemove at 924 556', 'clicker click at 22 414', 'clicker dblclick at 1 208', 'clicker dblclick at 1030 781', 'clicker click at 84 264', 'clicker click at 4 691', 'clicker mouseover at 1784 447', 'clicker mouseup at 226 550', 'clicker mouseover at 939 420', 'clicker mouseup at 178 652', 'clicker click at 1660 601', 'clicker mouseup at 25 301', 'clicker mouseover at 26 737', 'clicker click at 1586 760', 'clicker mouseout at 1878 992', 'clicker click at 1436 362', 'clicker dblclick at 734 662', 'clicker mouseover at 297 287', 'clicker click at 17 542', 'clicker dblclick at 1783 39', 'clicker mousemove at 1697 763', 'clicker mouseout at 1873 500', 'clicker mouseover at 1841 353', 'clicker click at 749 507', 'clicker mouseover at 263 277', 'clicker mousedown at 1640 153', 'clicker mousemove at 1000 898', 'clicker mouseover at 88 541', 'clicker mousemove at 1326 115', 'clicker mouseout at 888 548', 'clicker mouseover at 391 888', 'clicker click at 215 1076', 'clicker mousemove at 1423 53', 'clicker mouseover at 918 668', 'clicker mouseup at 1060 929', 'clicker dblclick at 1655 303', 'clicker mouseup at 1183 325', 'clicker mouseover at 627 408', 'clicker mouseover at 1277 326', 'clicker mouseover at 1196 494', 'clicker click at 982 752', 'clicker mousemove at 120 287', 'clicker mouseover at 1760 1066', 'clicker click at 1712 1016', 'clicker mousemove at 859 814', 'clicker mouseover at 1584 851', 'clicker click at 159 843', 'clicker click at 1697 938', 'clicker dblclick at 1235 36', 'clicker dblclick at 1906 783', 'clicker click at 1299 87', 'clicker click at 1136 521', 'clicker mouseover at 1325 684', 'clicker click at 276 379', 'clicker click at 1892 1001', 'clicker mouseout at 1508 374', 'clicker mouseover at 986 860', 'clicker dblclick at 669 322', 'clicker click at 1908 400', 'clicker mousemove at 1119 956', 'clicker click at 1013 854', 'clicker click at 1274 674', 'clicker mouseout at 1006 608', 'clicker click at 408 77', 'clicker dblclick at 1268 26', 'clicker click at 1247 270', 'clicker click at 645 161', 'clicker click at 1323 449', 'clicker mouseup at 1677 536', 'clicker dblclick at 1074 699', 'clicker dblclick at 1873 237', 'clicker dblclick at 328 303', 'clicker mouseup at 1653 900', 'clicker click at 833 1050', 'clicker dblclick at 682 1073', 'clicker mousemove at 737 869', 'clicker mouseover at 1722 51', 'clicker mouseover at 1749 278', 'clicker click at 1165 671', 'clicker mousedown at 679 38', 'clicker dblclick at 513 213', 'clicker click at 356 756', 'clicker mouseover at 841 1037', 'clicker click at 1838 562', 'clicker click at 1553 58', 'clicker click at 1739 48', 'clicker click at 1122 462', 'clicker click at 1320 196', 'clicker click at 1093 841', 'clicker mouseover at 366 1041', 'clicker mousedown at 721 1023', 'clicker mouseover at 582 1051', 'clicker mouseout at 1456 724', 'clicker click at 1200 171', 'clicker click at 614 301', 'clicker mouseover at 1493 776', 'clicker click at 1699 96', 'clicker click at 959 864', 'clicker mouseover at 1751 985', 'clicker mouseover at 924 24', 'clicker mouseup at 1891 316', 'clicker mouseout at 291 214', 'clicker click at 972 829', 'clicker click at 1828 1061', 'clicker mousedown at 473 906', 'clicker click at 1399 434', 'clicker mouseout at 1752 924', 'clicker dblclick at 1669 704', 'clicker mousemove at 299 198', 'clicker mouseout at 839 894', 'clicker dblclick at 1040 831', 'clicker click at 1402 723', 'clicker click at 624 582', 'clicker click at 1745 472', 'clicker click at 1497 457', 'clicker mouseover at 1564 382', 'clicker mouseover at 767 965', 'clicker mousedown at 818 420', 'clicker mouseover at 857 375', 'clicker click at 1859 693', 'clicker mouseover at 346 121', 'clicker mouseout at 996 947', 'clicker mouseover at 173 1042', 'clicker click at 1483 348', 'clicker mouseover at 828 829', 'clicker click at 975 891', 'clicker mousemove at 1321 521', 'clicker mousedown at 629 69', 'clicker dblclick at 561 24', 'clicker mouseup at 379 359', 'clicker click at 1140 523', 'clicker click at 471 485', 'clicker mouseover at 856 1008', 'clicker dblclick at 112 447', 'clicker mouseup at 402 921', 'clicker dblclick at 342 158', 'clicker click at 1581 288', 'clicker mousemove at 152 283', 'clicker click at 595 411', 'clicker click at 1652 133', 'clicker click at 676 385', 'clicker mousedown at 531 647', 'clicker click at 579 400', 'clicker click at 1235 170', 'clicker mouseup at 883 605', 'clicker dblclick at 1742 588', 'clicker dblclick at 1336 941', 'clicker click at 1789 359', 'clicker mouseout at 316 73', 'clicker mouseout at 719 896', 'clicker click at 1138 884', 'clicker click at 1633 1046', 'clicker click at 660 417', 'clicker mouseup at 1379 970', 'clicker click at 110 702', 'clicker click at 1048 643', 'clicker dblclick at 463 939', 'clicker click at 1344 648', 'clicker mouseover at 635 976', 'clicker mouseover at 1816 210', 'clicker dblclick at 117 657', 'clicker mouseover at 1653 1074', 'clicker click at 493 136', 'clicker click at 1890 538', 'clicker click at 359 470', 'clicker click at 530 500', 'clicker mouseover at 1176 796', 'clicker click at 756 441', 'clicker mousedown at 1761 325', 'clicker mouseover at 1590 923', 'clicker click at 59 614', 'clicker mousedown at 892 651', 'clicker click at 830 969', 'clicker mouseover at 1166 309', 'clicker click at 372 636', 'clicker click at 32 780', 'clicker mouseover at 801 525', 'clicker click at 1726 244', 'clicker click at 922 46', 'clicker mousedown at 203 143', 'clicker mouseout at 621 696', 'clicker dblclick at 143 984', 'clicker dblclick at 718 406', 'clicker dblclick at 1854 512', 'clicker click at 453 44', 'clicker mouseout at 1032 452', 'clicker mouseover at 1346 837', 'clicker mousemove at 34 291', 'clicker click at 805 670', 'clicker click at 1469 923', 'clicker dblclick at 199 59', 'clicker mousedown at 1301 788', 'clicker click at 327 11', 'clicker mouseover at 123 691', 'clicker dblclick at 102 373', 'clicker mouseover at 1907 386', 'clicker click at 1267 261', 'clicker click at 1290 540', 'clicker dblclick at 1198 181', 'clicker mouseout at 232 539', 'clicker mouseover at 1714 320', 'clicker mouseover at 442 521', 'clicker click at 728 698', 'clicker mousemove at 522 699', 'clicker click at 117 921', 'clicker mouseover at 1188 509', 'clicker mousemove at 816 1063', 'clicker mouseover at 729 313']
			},
 			{"history_index": None,  "crowding_dist": None, "fitness":  {"valid": False,"values": None},"sequence":
			["clicker click at 39 896","clicker click at 1487 605","clicker mousemove at 1463 550","clicker click at 785 139","clicker click at 503 15","clicker click at 217 359","clicker mousedown at 975 198","clicker mouseup at 1713 176","clicker click at 408 327","clicker click at 1395 625","clicker click at 1068 224","clicker mouseover at 1839 748","clicker mouseover at 1222 932","clicker click at 380 792","clicker dblclick at 1155 0","clicker mouseover at 1079 375","clicker dblclick at 93 1002","clicker click at 1403 57","clicker mouseup at 1032 418","clicker click at 1846 914","clicker click at 1644 618","clicker click at 445 38","clicker mouseup at 536 950","clicker mousedown at 178 324","clicker click at 452 584","clicker click at 714 989","clicker click at 1744 387","clicker mousedown at 582 516","clicker mouseover at 785 715","clicker dblclick at 881 165","clicker mouseup at 1299 29","clicker mouseover at 1728 738","clicker mousedown at 235 223","clicker mousemove at 1162 196","clicker mouseover at 32 770","clicker mouseout at 389 437","clicker mouseover at 1076 35","clicker click at 480 356","clicker mouseover at 640 1006","clicker mouseover at 455 1070","clicker mouseover at 626 130","clicker click at 1289 264","clicker dblclick at 411 829","clicker click at 1494 72","clicker dblclick at 128 944","clicker mouseout at 242 405","clicker click at 1347 879","clicker mouseout at 485 46","clicker mouseout at 1020 976","clicker mouseover at 1106 307","clicker mousedown at 1337 403","clicker mouseover at 919 52","clicker mousemove at 1604 662","clicker click at 1885 830","clicker click at 1669 825","clicker mousemove at 510 917","clicker mouseover at 242 1016","clicker mouseover at 1479 1","clicker mousemove at 43 860","clicker mouseover at 762 598","clicker click at 1544 80","clicker dblclick at 667 916","clicker click at 569 289","clicker click at 54 315","clicker mouseout at 708 64","clicker click at 591 1041","clicker dblclick at 1438 602","clicker mousemove at 1523 426","clicker click at 758 294","clicker click at 1876 972","clicker mouseup at 1449 150","clicker click at 988 839","clicker click at 1149 905","clicker click at 1152 577","clicker click at 1529 312","clicker mousedown at 506 506","clicker mousedown at 192 805","clicker mouseover at 328 365","clicker mousemove at 615 758","clicker mouseover at 656 574","clicker mouseover at 188 18","clicker click at 72 83","clicker dblclick at 158 195","clicker dblclick at 1511 984","clicker mouseover at 1326 794","clicker dblclick at 649 612","clicker click at 1573 697","clicker click at 206 280","clicker mouseup at 1395 419","clicker click at 1224 171","clicker mouseover at 163 366","clicker click at 192 873","clicker click at 1076 1018","clicker mouseover at 1765 473","clicker mouseover at 1633 216","clicker click at 90 772","clicker click at 387 767","clicker dblclick at 1579 909","clicker dblclick at 1069 385","clicker mouseout at 784 137","clicker click at 1768 908","clicker mouseout at 1394 886","clicker mouseover at 365 331","clicker dblclick at 166 741","clicker click at 595 717","clicker click at 1056 482","clicker mouseup at 112 790","clicker mouseover at 946 1037","clicker click at 1597 866","clicker dblclick at 1840 611","clicker mouseover at 140 642","clicker mouseover at 749 29","clicker mouseup at 1320 980","clicker click at 1039 842","clicker dblclick at 1325 642","clicker mouseover at 1150 778","clicker click at 176 926","clicker click at 1264 53","clicker mouseup at 530 611","clicker mouseover at 804 229","clicker click at 1356 643","clicker mousedown at 1723 555","clicker click at 1047 825","clicker click at 331 434","clicker click at 528 820","clicker click at 515 790","clicker click at 795 532","clicker click at 551 973","clicker click at 1128 217","clicker click at 773 175","clicker mousedown at 260 742","clicker click at 342 464","clicker mouseup at 1691 712","clicker dblclick at 48 418","clicker mouseout at 1714 1065","clicker mouseup at 1600 488","clicker click at 1768 767","clicker mouseover at 1360 775","clicker dblclick at 634 535","clicker mousemove at 1849 349","clicker mousedown at 1703 427","clicker click at 1078 236","clicker mouseover at 1315 1027","clicker mousedown at 1581 319","clicker click at 104 1034","clicker mouseup at 207 102","clicker click at 948 755","clicker mouseover at 486 258","clicker mouseover at 916 890","clicker mouseup at 1170 55","clicker mouseout at 632 270","clicker mouseover at 834 914","clicker mousedown at 1860 882","clicker mousemove at 598 558","clicker click at 233 920","clicker mouseover at 829 746","clicker click at 1602 631","clicker dblclick at 1056 565","clicker mouseout at 1532 518","clicker dblclick at 1240 592","clicker click at 71 285","clicker click at 212 216","clicker mouseout at 431 683","clicker mouseout at 377 364","clicker click at 130 909","clicker click at 386 427","clicker mouseout at 1858 613","clicker click at 479 840","clicker mouseout at 1455 231","clicker mouseover at 1531 629","clicker click at 471 180","clicker click at 470 364","clicker click at 1020 126","clicker mousemove at 41 433","clicker click at 1217 696","clicker click at 1615 458","clicker dblclick at 209 22","clicker click at 1611 800","clicker click at 1192 692","clicker click at 1741 186","clicker click at 867 94","clicker mousemove at 334 1035","clicker mouseover at 756 90","clicker mouseover at 837 87","clicker mousedown at 1474 178","clicker click at 1718 583","clicker click at 1898 870","clicker mouseover at 954 555","clicker click at 761 129","clicker mousedown at 232 467","clicker mousemove at 705 1078","clicker mouseover at 54 424","clicker click at 411 557","clicker mouseover at 945 317","clicker click at 1187 622","clicker click at 478 175","clicker click at 1637 360","clicker mouseover at 283 542","clicker click at 285 427","clicker mouseout at 171 657","clicker dblclick at 958 749","clicker mouseover at 847 1035","clicker click at 548 670","clicker mouseup at 1419 560","clicker click at 529 1011","clicker click at 1725 1000","clicker mouseover at 1548 115","clicker mouseover at 10 199","clicker click at 875 947","clicker dblclick at 1318 659","clicker click at 696 732","clicker dblclick at 361 356","clicker mouseover at 1142 983","clicker mouseout at 1663 427","clicker click at 807 154","clicker dblclick at 586 958","clicker click at 257 184","clicker dblclick at 1415 281","clicker mouseout at 1697 107","clicker mouseout at 328 17","clicker click at 944 701","clicker click at 1433 622","clicker mouseover at 1579 848","clicker dblclick at 198 831","clicker mousedown at 744 979","clicker mouseout at 1022 8","clicker click at 376 245","clicker click at 1363 788","clicker click at 365 717","clicker mousemove at 1405 656","clicker mouseover at 838 534","clicker click at 1824 738","clicker click at 1902 973","clicker click at 819 449","clicker dblclick at 238 613","clicker click at 1917 1050","clicker mouseover at 1479 57","clicker click at 415 331","clicker click at 1655 60","clicker click at 1275 688","clicker mouseover at 1005 895","clicker dblclick at 549 495","clicker click at 1006 131","clicker click at 663 350","clicker dblclick at 966 321","clicker click at 28 819","clicker mouseout at 570 690","clicker click at 908 374","clicker mouseup at 1842 214","clicker mousedown at 434 36","clicker dblclick at 1030 913","clicker click at 1620 789","clicker mouseout at 1775 297","clicker mouseover at 1213 839","clicker click at 720 342"]  			},
   			{"history_index": None, "crowding_dist": None,  "fitness":  {"valid": False,"values": None},"sequence":
			["clicker dblclick at 1227 1064","clicker mouseover at 1443 854","clicker click at 784 932","clicker mousemove at 1274 390","clicker mouseover at 281 789","clicker dblclick at 1154 158","clicker dblclick at 1009 565","clicker mousedown at 708 242","clicker mouseover at 1582 845","clicker mouseover at 232 433","clicker mouseout at 684 535","clicker click at 1557 667","clicker click at 1216 502","clicker click at 1405 668","clicker mousedown at 490 413","clicker click at 716 1027","clicker click at 1365 795","clicker click at 1368 1059","clicker dblclick at 1919 238","clicker click at 1834 1039","clicker click at 1049 1041","clicker click at 1216 483","clicker click at 1910 1009","clicker mouseover at 1644 445","clicker dblclick at 1705 294","clicker click at 1622 629","clicker click at 548 905","clicker mouseover at 1059 510","clicker mouseover at 1506 742","clicker mouseover at 1228 531","clicker mouseout at 1410 758","clicker click at 1794 1025","clicker click at 914 558","clicker click at 656 361","clicker mousemove at 89 500","clicker mousedown at 407 562","clicker mousedown at 685 985","clicker mouseover at 1735 398","clicker mouseup at 1066 1031","clicker mouseout at 228 930","clicker mouseup at 1124 243","clicker click at 1425 966","clicker mouseout at 37 909","clicker dblclick at 379 184","clicker dblclick at 334 544","clicker mousedown at 1506 50","clicker mousedown at 882 708","clicker dblclick at 1369 1012","clicker mouseup at 991 1005","clicker mouseover at 114 88","clicker mouseover at 194 1036","clicker mouseup at 1308 538","clicker mousemove at 1818 917","clicker click at 1434 751","clicker mousedown at 1805 152","clicker click at 1632 69","clicker click at 206 303","clicker click at 58 929","clicker mouseover at 297 454","clicker mousemove at 1847 806","clicker mousemove at 924 556","clicker click at 22 414","clicker dblclick at 1027 430","clicker click at 1013 341","clicker mouseout at 1159 328","clicker click at 1283 148","clicker mousemove at 1673 246","clicker dblclick at 1438 359","clicker mouseover at 939 420","clicker mousemove at 1411 243","clicker mouseover at 1274 496","clicker mousemove at 666 692","clicker dblclick at 1829 721","clicker mouseover at 687 1062","clicker mouseout at 1878 992","clicker click at 704 748","clicker click at 156 539","clicker mousedown at 608 968","clicker click at 1211 1052","clicker mouseover at 1196 723","clicker click at 1358 574","clicker click at 952 982","clicker mousedown at 1428 553","clicker dblclick at 1578 963","clicker mousemove at 334 356","clicker mousedown at 1640 153","clicker mousemove at 1000 898","clicker mousedown at 559 700","clicker mousemove at 1326 115","clicker mouseout at 888 548","clicker mousedown at 969 863","clicker mouseover at 1343 538","clicker mousemove at 1374 497","clicker mouseout at 1370 899","clicker mousemove at 1367 1010","clicker dblclick at 1655 303","clicker mouseup at 1183 325","clicker mouseover at 402 330","clicker mouseup at 242 432","clicker mousemove at 27 148","clicker click at 573 478","clicker mouseover at 291 861","clicker mouseup at 226 73","clicker mouseup at 273 128","clicker click at 454 946","clicker mousemove at 198 116","clicker click at 1740 879","clicker click at 1697 938","clicker dblclick at 740 937","clicker dblclick at 1906 783","clicker mouseover at 502 308","clicker click at 1053 744","clicker mouseover at 1325 684","clicker click at 518 849","clicker mouseout at 1010 516","clicker mouseover at 1789 986","clicker click at 506 816","clicker click at 352 620","clicker click at 1908 400","clicker mousedown at 1825 608","clicker click at 662 559","clicker click at 1274 674","clicker mouseout at 1207 347","clicker click at 408 77","clicker dblclick at 1268 26","clicker click at 1247 270","clicker click at 1584 504","clicker mouseover at 1895 325","clicker mouseup at 1677 536","clicker mouseover at 1779 212","clicker click at 315 972","clicker dblclick at 325 1003","clicker click at 1141 363","clicker click at 833 1050","clicker dblclick at 682 1073","clicker mousemove at 737 869","clicker click at 1184 995","clicker mouseover at 1749 278","clicker mouseover at 1530 422","clicker mouseup at 846 982","clicker click at 1904 538","clicker mouseout at 404 38","clicker mousedown at 1903 470","clicker mouseover at 1185 566","clicker mouseout at 914 693","clicker mouseover at 597 666","clicker click at 1122 462","clicker mousedown at 1590 760","clicker click at 1017 925","clicker mouseover at 399 136","clicker click at 675 123","clicker mouseup at 1211 231","clicker click at 430 912","clicker mousemove at 149 253","clicker click at 614 301","clicker mousemove at 806 465","clicker mousedown at 1168 163","clicker click at 526 926","clicker mouseover at 1751 985","clicker mouseover at 928 65","clicker mouseup at 1891 316","clicker mouseout at 291 214","clicker click at 972 829","clicker dblclick at 1265 696","clicker dblclick at 1903 812","clicker mouseup at 311 956","clicker click at 554 888","clicker dblclick at 1669 704","clicker mousemove at 299 198","clicker dblclick at 902 118","clicker mouseover at 187 330","clicker click at 1402 723","clicker click at 624 582","clicker click at 923 418","clicker mouseover at 59 1074","clicker click at 1090 527","clicker mouseover at 767 965","clicker mouseout at 1421 718","clicker mouseup at 97 258","clicker mouseover at 563 683","clicker mousemove at 450 1058","clicker mouseout at 996 947","clicker mouseover at 889 141","clicker click at 1483 348","clicker mouseover at 828 829","clicker click at 975 891","clicker mousedown at 1547 814","clicker click at 1869 622","clicker click at 1437 505","clicker mouseover at 444 34","clicker mouseover at 1737 804","clicker dblclick at 1445 990","clicker mouseover at 1893 821","clicker mousedown at 330 675","clicker dblclick at 608 128","clicker mousemove at 894 264","clicker mouseover at 528 390","clicker click at 207 741","clicker mouseover at 588 751","clicker dblclick at 156 681","clicker click at 676 385","clicker dblclick at 56 351","clicker mouseover at 1817 119","clicker dblclick at 1248 155","clicker mouseout at 497 388","clicker click at 1017 828","clicker dblclick at 1293 648","clicker click at 1163 763","clicker click at 1288 631","clicker click at 515 63","clicker click at 775 408","clicker click at 134 968","clicker click at 1811 260","clicker mouseup at 1379 970","clicker mouseover at 246 979","clicker mouseout at 739 125","clicker dblclick at 469 167","clicker click at 1344 648","clicker mouseup at 65 306","clicker click at 361 934","clicker click at 1326 533","clicker click at 204 1043","clicker click at 493 136","clicker click at 1890 538","clicker click at 1712 359","clicker mouseover at 248 545","clicker click at 547 962","clicker click at 756 441","clicker dblclick at 1065 460","clicker click at 746 516","clicker click at 59 614","clicker click at 986 287","clicker click at 1563 821","clicker mouseover at 1166 309","clicker click at 1673 445","clicker mouseup at 138 674","clicker click at 455 584","clicker dblclick at 1230 862","clicker click at 1267 436","clicker dblclick at 1360 138","clicker mouseout at 126 654","clicker dblclick at 143 984","clicker click at 896 693","clicker mouseover at 1779 675","clicker mouseover at 425 828","clicker mouseover at 1415 565","clicker mouseover at 1346 837","clicker mousemove at 34 291","clicker click at 799 298","clicker mouseover at 1770 889","clicker mouseover at 553 35","clicker click at 115 133","clicker click at 1855 878","clicker mouseout at 1889 832","clicker dblclick at 1604 494","clicker mouseover at 1907 386","clicker mouseover at 1805 846","clicker mouseover at 1353 817","clicker click at 785 281","clicker mousedown at 1840 954","clicker dblclick at 1554 127","clicker mousemove at 849 223","clicker click at 728 698","clicker click at 1481 419","clicker click at 1389 875","clicker mouseover at 1188 509","clicker click at 336 42","clicker click at 9 14"]   			
   			}
   			]
	return suite


# the suite coverage is accumulated
def eval_suite(individual, gen, pop):
	# for get_motifcore_suite_coverage
	# script_path = []

	# for length objective
	# suite_lengths = []
	# for index, seq in enumerate(individual):
	# generate script file list
	# script = open("./intermediate/motifcore.evo.script." + str(gen) + "." + str(pop), "w")
	# print(individual["sequence"])
	# script.write(individual["sequence"])
	script = open("./intermediate/test"+ str(gen) + "." + str(pop) + ".pickle", 'wb')
	pickle.dump(individual["sequence"], script)
	script.close()
 
		# length = 0
		# for line in seq:
		# 	script.write(line + "\n")
		# 	length += 1
 
	print ("### Individual Lengths: ", len(individual["sequence"]))
	suite_length = len(individual["sequence"])

	# TODO: Persiste steps


	# print(individual)
	# print('before')
	coverage = reproRunner.reproAndCoverage(individual["sequence"])
	# print('after')
  # TODO: Add coverage and length here!
	# give a script and package, return the coverage by running all seqs
	# if apk_dir.endswith(".apk_output"):
	# 	coverage, num_crashes = act_coverage.get_suite_coverage(script_path, device, apk_dir, package_name, gen, pop)
	# else:
	# 	coverage, num_crashes = emma_coverage.get_suite_coverage(script_path, device, apk_dir, package_name, gen, pop)
	# print ("### Coverage = ", coverage)
	# print ("### Length = ", suite_length)
	# print ("### #Crashes = ", 0)
 
	# 1st obj: coverage, 2nd: average seq length of the suite, 3nd: #crashes
	return pop, (coverage, suite_length, 0)


def mut_suite(individual, indpb):
	# shuffle seq
	individual, = tools.mutShuffleIndexes(individual, indpb)

	# crossover inside the suite
	for i in range(1, len(individual), 2):
		if random.random() < settings.MUTPB:
			if len(individual[i - 1]) <= 2:
				print ("\n\n### Indi Length =", len(individual[i - 1]), " ith = ", i - 1, individual[i - 1])
				continue  # sys.exit(1)
			if len(individual[i]) <= 2:
				print ("\n\n### Indi Length =", len(individual[i]), "ith = ", i, individual[i])
				continue  # sys.exit(1)

			individual[i - 1], individual[i] = tools.cxOnePoint(individual[i - 1], individual[i])

	# shuffle events
	for i in range(len(individual)):
		if random.random() < settings.MUTPB:
			if len(individual[i]) <= 2:
				print ("\n\n### Indi Length =", len(individual[i]), "ith = ", i, individual[i])
				continue  # sys.exit(1)
			individual[i], = tools.mutShuffleIndexes(individual[i], indpb)

	return individual,


def return_as_is(a):
	return a


# def initRepeat(container, func, n):
	# return container(func() for _ in xrange(n))

### deap framework setup
creator.create("FitnessCovLen", base.Fitness, weights=(10.0, -0.5, 1000.0))
creator.create("Individual", list, fitness=creator.FitnessCovLen)

toolbox = base.Toolbox()

toolbox.register("individual", gen_individual)

toolbox.register("population", initRepeatParallel.initPop, list, toolbox.individual)

toolbox.register("evaluate", eval_suite)
# mate crossover two suites
toolbox.register("mate", tools.cxUniform, indpb=0.5)
# mutate should change seq order in the suite as well
toolbox.register("mutate", mut_suite, indpb=0.5)
# toolbox.register("select", tools.selTournament, tournsize=5)
toolbox.register("select", tools.selNSGA2)

# log the history
history = tools.History()
# Decorate the variation operators
toolbox.decorate("mate", history.decorator)
toolbox.decorate("mutate", history.decorator)


def get_package_name(path):
	apk_path = None
	if path.endswith(".apk"):
		apk_path = path
	else:
		for file_name in os.listdir(path + "/bin"):
			if file_name == "bugroid-instrumented.apk":
				apk_path = path + "/bin/bugroid-instrumented.apk"
				break
			elif file_name.endswith("-debug.apk"):
				apk_path = path + "/bin/" + file_name

	assert apk_path is not None

	get_package_cmd = "aapt d xmltree " + apk_path + " AndroidManifest.xml | grep package= | awk 'BEGIN {FS=\"\\\"\"}{print $2}'"
	# print get_package_cmd
	package_name = subprocess.Popen(get_package_cmd, shell=True, stdout=subprocess.PIPE).communicate()[0].strip()
	return package_name, apk_path


def main(instrumented_app_dir):
	"""
	Test one apk
	:param instrumented_app_dir: The instrumentation folder of the app | apk file path for closed-source app
	"""

	# host_system = platform.system()
	# if host_system == "Darwin":
	# 	print ("Running on Mac OS")
	# 	settings.TIMEOUT_CMD = "gtimeout"
	# elif host_system == "Linux":
	# 	print ("Running on Linux")
	# else:
	# 	print ("Runnning on unknown OS")

	# package_name, apk_path = get_package_name(instrumented_app_dir)
	# # for css subjects
	# if instrumented_app_dir.endswith(".apk"):
	# 	instrumented_app_dir += "_output"
	# 	os.system("mkdir " + instrumented_app_dir)

	# print ("### Working on apk:", package_name)

	# get emulator device
	# print ("Preparing devices ...")
	# emulator.boot_devices()
	# emulator.prepare_motifcore()
	# emulator.clean_sdcard()

	# log the devices
	# devices = emulator.get_devices()

	# static analysis
	# if settings.ENABLE_STRING_SEEDING:
	# 	output_dir = None
	# 	if instrumented_app_dir.endswith(".apk_output"):
	# 		output_dir = instrumented_app_dir
	# 	else:
	# 		output_dir = instrumented_app_dir + "/bin"
	# 	static_analyser.decode_apk(apk_path, output_dir)
	# # will use dummy 0 if disabled
	# for device in devices:
	# 	decoded_dir = None
	# 	if instrumented_app_dir.endswith(".apk_output"):
	# 		decoded_dir = instrumented_app_dir + "/" + apk_path.split("/")[-1].split(".apk")[0]
	# 	else:
	# 		decoded_dir = instrumented_app_dir + "/bin/" + apk_path.split("/")[-1].split(".apk")[0]
	# 	static_analyser.upload_string_xml(device, decoded_dir, package_name)

	# 	os.system("adb -s " + device + " shell rm /mnt/sdcard/bugreport.crash")
	# 	os.system("adb -s " + device + " uninstall " + package_name)
	# 	os.system("adb -s " + device + " install " + apk_path)

	# intermediate should be in app folder
	os.system("rm -rf " + instrumented_app_dir + "/intermediate")
	os.system("mkdir " + instrumented_app_dir + "/intermediate")

	# os.system("rm -rf " + instrumented_app_dir + "/crashes")
	# os.system("mkdir " + instrumented_app_dir + "/crashes")

	# os.system("rm -rf " + instrumented_app_dir + "/coverages")
	# os.system("mkdir " + instrumented_app_dir + "/coverages")

	# generate initial population
	print ("### Initialising population ....")

	population = toolbox.population(n=settings.POPULATION_SIZE)
  
	# print (population)
 
	# print ("### Individual Lengths: ")
	# for indi in population:
	# 	for seq in indi:
	# 		print (len(seq))
	# 	print ("")

	history.update(population)
 
	# print(population)

	# hof = tools.HallOfFame(6)
	# pareto front can be large, there is a similarity option parameter
	hof = tools.ParetoFront()
	# print ('hof', hof)
 
	# print(ind["fitness"]["values"])

	stats = tools.Statistics(lambda ind: ind["fitness"]["values"])
	# axis = 0, the numpy.mean will return an array of results
	stats.register("avg", numpy.mean, axis=0)
	stats.register("std", numpy.std, axis=0)
	stats.register("min", numpy.min, axis=0)
	stats.register("max", numpy.max, axis=0)
	stats.register("pop_fitness", return_as_is)

	# evolve
	print ("### Start to Evolve")
	population, logbook = eaMuPlusLambdaParallel.evolve(population, toolbox, settings.POPULATION_SIZE,
														settings.OFFSPRING_SIZE,
														cxpb=settings.CXPB, mutpb=settings.MUTPB,
														ngen=settings.GENERATION,
              											apk_dir=instrumented_app_dir,
														stats=stats, halloffame=hof, verbose=True)

	# persistent
	logbook_file = open(instrumented_app_dir + "/intermediate/logbook.pickle", 'wb')
	pickle.dump(logbook, logbook_file)
	logbook_file.close()

	hof_file = open(instrumented_app_dir + "/intermediate/hof.pickle", 'wb')
	pickle.dump(hof, hof_file)
	hof_file.close()

	history_file = open(instrumented_app_dir + "/intermediate/history.pickle", 'wb')
	pickle.dump(history, history_file)
	history_file.close()
 
	print ("### Finished persist")

	# draw graph
	two_d_line.plot(logbook, 0, instrumented_app_dir)
	two_d_line.plot(logbook, 1, instrumented_app_dir)
	two_d_line.plot(logbook, 2, instrumented_app_dir)


# draw history network
# history_network.plot(history, instrumented_app_dir)


if __name__ == "__main__":
	app_dir = sys.argv[1]
	main(app_dir)
