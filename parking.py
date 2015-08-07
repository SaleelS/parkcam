import gspread
from difflib import SequenceMatcher
import subprocess
import json
import sys
import shlex
from openpyxl import load_workbook

class PlateReader:
    #@param carImage is a filename string
    #DONT UNFOLD contains pw lol
    def __init__(self):
        self.gdoc = self.getGdoc()
    def alpr_subprocess(self):
        alpr_args = shlex.split(self.alpr_command_args)
        return subprocess.Popen(alpr_args, stdout = subprocess.PIPE)

    def alpr_json_results(self):
        alpr_out, alpr_error = self.alpr_subprocess().communicate()

        if not alpr_error is None:
            return None, alpr_error
        elif "No license plates found." in alpr_out:
            return None, None

        try:
            return json.loads(alpr_out), None
        except ValueError, e:
            return None, e


    def read_plate(self,image):
        self.alpr_command_args = "alpr -j " + image
        alpr_json, alpr_error = self.alpr_json_results()

        if not alpr_error is None:
            print alpr_error
            return

        if alpr_json is None:
            print "No results!"
            return

        results = alpr_json["results"][0]
        return results['plate']

    def getGdoc(self):
        """
        parkerC = gspread.Client(self.auth)
        parkerC.login()
        parkerS = parkerC.open_by_key("18pus8l5KnrdThVcTrylR3Zvj1Pmgs8L8QocJACImFTU")
        parker = parkerS.get_worksheet(0)
        return parker
        """
        wb = load_workbook('parking.xlsx')
        return wb.get_sheet_by_name("Sheet1")

    def getRowbyPlate(self,plate):
        parker = self.gdoc
        plates = [a[0].value for a in parker["D2:D257"]]
        names = [a[0].value for a in parker["A2:A257"]]
        #print plates
        maxMatch = 0
        matchIdx = -1
        for i in range(len(plates)):
            if plates[i] is None:
                continue
            matcher = SequenceMatcher(None,plates[i],plate)
            mp = matcher.ratio()
            if mp > maxMatch:
                matchIdx = i
                maxMatch = mp
        if maxMatch > 0.5:
            print matchIdx
            return names[matchIdx]
        else:
            return None

def __main__():
    args = sys.argv[1:]
    if len(sys.argv) != 2:
        print("please enter an image to process")
        exit(1)
    else:
        pr = PlateReader()
        plate = pr.read_plate(args[0])
        print(pr.getRowbyPlate(plate))



def readPlate(carImageFile):
    subprocess

if __name__ == "__main__":
    __main__()