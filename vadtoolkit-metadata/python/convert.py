import os

import pandas as pd
from scipy.io import loadmat
import numpy as np

from audata import define
from audata import utils
from audata import Database, Scheme, Column, Table, AudioInfo


def convert(description: str, data_root: str, annotation_root: str) \
            -> Database:

    audio_file_ext = '.wav'
    anno_file_ext = '.mat'
    sampling_rate = 16000

    db = Database(
        name='vadtoolkit',
        source='https://github.com/jtkim-kaist/VAD',
        usage=define.Usage.COMMERCIAL,
        languages=[utils.str_to_language('kor')],
        description=description)

    #########
    # Media #
    #########

    db.media['microphone'] = AudioInfo(sampling_rate=sampling_rate, channels=1,
                                       format='wav')

    #########
    # Files #
    #########

    files = list(utils.scan_files(data_root, pattern='*' + audio_file_ext))
    files.sort()

    ##########
    # Values #
    ##########

    def parse_annotation(file):
        path = os.path.join(data_root, file.replace(audio_file_ext,
                                                    anno_file_ext))
        y = loadmat(path)['y_label'].squeeze().astype(np.int8)
        y_d = np.diff(y)
        y_start = pd.to_timedelta(np.where(y_d == 1)[0]
                                  / sampling_rate, unit='s')
        y_end = pd.to_timedelta(np.where(y_d == -1)[0]
                                / sampling_rate, unit='s')
        df = pd.DataFrame(data={
            'start': y_start,
            'end': y_end})
        df['file'] = file
        df.set_index(['file', 'start', 'end'], inplace=True)
        return df

    annotations = utils.run_worker_threads(
        num_workers=len(files),
        task_fun=parse_annotation,
        params=[os.path.join(file) for file in files],
        progress_bar=True)
    annotations = pd.concat(annotations, axis=0)

    ##########
    # Tables #
    ##########

    db['segments'] = Table(files=annotations)

    return db
