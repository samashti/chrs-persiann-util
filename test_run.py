from chrs_persiann import CHRS


def main():

    params = {
        'start': '2021010100',
        'end': '2021010300',
        'mailid': 'test@gmail.com',
        'download_path': '~/Downloads',
        'file_format': 'Tif',
        'timestep': 'daily',
        'compression': 'zip'
    }

    dl = CHRS()

    # PERSIANN
    dl.get_persiann(**params)

    # PERSIANN CCS
    dl.get_persiann_ccs(**params)

    # PERSIANN CDR
    dl.get_persiann_cdr(**params)

    # PDIR-Now
    dl.get_pdir(**params)

    pass


if __name__ == '__main__':
    main()
