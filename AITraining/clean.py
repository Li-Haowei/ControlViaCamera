# there is a hand_dataset folder in the same directory as this file
# inside the hand_dataset folder there are 4 folders: Clic, No, Rotate, StopGraspOk
# Clic has Seq1, Seq2, Seq3, Seq4, Seq5, Seq6, Seq7, Seq8, Seq9, Seq10, Seq11, Seq12, Seq13, Seq14, Seq15
# No has Seq1, Seq2, Seq3, Seq4, Seq5, Seq6, Seq7, Seq8, Seq9, Seq10, Seq11, Seq12, Seq13, Seq14
# Rotate has Seq1, Seq2, Seq3, Seq4, Seq5, Seq6, Seq7, Seq8, Seq9, Seq10, Seq11, Seq12, Seq13
# StopGraspOk has Seq1, Seq2, Seq3, Seq4, Seq5, Seq6, Seq7, Seq8, Seq9, Seq10, Seq11, Seq12, Seq13, Seq14, Seq15

# move all pnm images inside these Seq folders to the hand_dataset folder

import os
import shutil

# get the current working directory
cwd = os.getcwd()
cwd+='\AITraining'

# get the path to the hand_dataset folder
hand_dataset_path = os.path.join(cwd, 'hand_dataset')

def moveAllPNMFileToPath(hand_dataset_path):
    # get the list of folders inside the hand_dataset folder
    folders = os.listdir(hand_dataset_path)

    # loop through the folders
    for folder in folders:
        # get the path to the folder
        folder_path = os.path.join(hand_dataset_path, folder)
        # get the list of folders inside the folder
        subfolders = os.listdir(folder_path)
        # loop through the subfolders
        for subfolder in subfolders:
            # get the path to the subfolder
            subfolder_path = os.path.join(folder_path, subfolder)
            # get the list of files inside the subfolder
            files = os.listdir(subfolder_path)
            # loop through the files
            for file in files:
                # get the path to the file
                file_path = os.path.join(subfolder_path, file)
                # check if the file is a pnm file
                if file.endswith('.pnm'):
                    # append the folder name to the beginning of the file name
                    new_file_name = folder + '_' + file
                    # get the path to the new file
                    new_file_path = os.path.join(hand_dataset_path, new_file_name)
                    # move the file to the hand_dataset folder
                    shutil.move(file_path, new_file_path)

def removeAllPNMFileFromPath(hand_dataset_path):
    """
    This function removes all pnm files from the hand_dataset_path
    """
    files = os.listdir(hand_dataset_path)
    for file in files:
        file_path = os.path.join(hand_dataset_path, file)
        if file.endswith('.pnm'):
            os.remove(file_path)

moveAllPNMFileToPath(hand_dataset_path)