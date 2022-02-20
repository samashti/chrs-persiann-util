
import os
import json
import requests

from pathlib import Path


class CHRS:

    def __init__(self) -> None:
        pass

    @staticmethod
    def download(url: str, filepath: str):
        """Download the file url using the chunks/stream option

        Args:
            url (str): url of the file to be downloaded

            filepath (str): destination of the file

        Returns:
            (bool): True if completed successfully
        """
        response = requests.get(url, stream=True)
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=2048):
                if chunk:
                    f.write(chunk)
                    f.flush()
        return True

    @staticmethod
    def query_url(start: str, end: str, data_type: str, file_format: str = 'Tif',
                  timestep: str = 'monthly', compression: str = 'zip'):
        """This function queries for the data with the supplied parameters for
        data type, period, time step, file format. And places an order for the
        data generation.

        Args:
            start (str): start date in 'yyyymmddHH' format
                        HH for 1hrly - 00, 01, ---, 23

                        HH for 3hrly - 00, 03, 06, 09, 12, 15, 18, 21

                        HH for 6hrly - 00, 06, 12, 18

            end (str): end date in 'yyyymmddHH' format
                        HH for 1hrly - 00, 01, ---, 23

                        HH for 3hrly - 00, 03, 06, 09, 12, 15, 18, 21

                        HH for 6hrly - 00, 06, 12, 18

            data_type (str): Data Collection to be downloaded
                        options:
                            PERSIANN -> PERSIANN,
                            CCS -> PERSIANN-CCS,
                            CDR -> PERSIANN-CDR,
                            PDIR -> PDIR

            file_format (str, optional): File format for the data to be downloaded.
                        options:
                            ArcGrid,
                            Tif,
                            NetCDF
                        Defaults to 'Tif'.

            timestep (str, optional): Time step/interval for the subsequent data
                        files in the time period.
                        options:
                            1hrly,
                            3hrly,
                            6hrly,
                            daily,
                            monthly,
                            yearly,
                        Defaults to 'monthly'.

            compression (str, optional): Download file format.
                        options:
                            zip, 
                            tar (in development)
                        Defaults to 'zip'.

        Returns:
            body (str): json result of query If Successful else None
        """

        folder = {
            'PERSIANN': 'PERSIANN',
            'CCS': 'PERSIANN-CCS',
            'CDR': 'PERSIANN-CDR',
            'PDIR': 'PDIR'
        }

        formats = ['ArcGrid', 'Tif', 'NetCDF']
        compress_formats = ['zip']  # , 'tar'] - # TODO: add tar case

        timestep_dict = {
            '1hrly': '1h',
            '3hrly': '3h',
            '6hrly': '6h',
            'daily': '1d',
            'monthly': '1m',
            'yearly': '1y',
            # 'accumulative': 'acc' # TODO: add accumulative case
        }

        if timestep not in timestep_dict.keys():
            print('Please provide a valid timestep for the period')
            return None

        if file_format not in formats:
            print('Please provide a valid data format for the download')
            return None

        if compression not in compress_formats:
            print('Please provide a valid compression format for the data download')
            return None

        if data_type not in folder.keys():
            print('Please provide the correct data type.')
            return None

        # TODO: Check the input date format is correct

        timestep_alt = timestep_dict[timestep.lower()]

        if 'h' in timestep_alt or 'acc' in timestep_alt:
            start_time = start
            end_time = end
        elif 'd' in timestep_alt:
            start_time = start[:8]
            end_time = end[:8]
        elif 'm' in timestep_alt:
            start_time = start[:6]
            end_time = end[:6]
        elif 'y' in timestep_alt:
            start_time = start[:4]
            end_time = end[:4]

        query_url = 'https://chrsdata.eng.uci.edu/php/downloadWholeData.php'

        # query_url = f'https://chrsdata.eng.uci.edu/php/downloadWholeData.php?
        # startDate={startmonth}&endDate={endmonth}&timestep=monthly&dataType=CCS
        # &format=Tif&compression=zip&timestepAlt=1m'

        params = {
            'startDate': start_time,
            'endDate': end_time,
            'timestep': timestep,
            'timestepAlt': timestep_alt,
            'dataType': data_type,
            'format': file_format,
            'compression': compression
        }

        try:
            query = requests.get(query_url, params=params)
            if query.status_code != 200:
                raise Exception('Null Response')

            body = json.loads(query.text)
            return body

        except Exception:
            return None

    @staticmethod
    def generate_url(start: str, end: str, userip: str, zipFile: str, mailid: str,
                     data_type: str, compression: str, timestep: str):
        """This function generates the url for the ordered data file from the
        result of the query. The returned file url can be used to download the
        compressed data file containing all the files in the requested format.

        Args:
            start (str): start date in 'yyyymmddHH' format
                        HH for 1hrly - 00, 01, ---, 23

                        HH for 3hrly - 00, 03, 06, 09, 12, 15, 18, 21

                        HH for 6hrly - 00, 06, 12, 18

            end (str): end date in 'yyyymmddHH' format
                        HH for 1hrly - 00, 01, ---, 23

                        HH for 3hrly - 00, 03, 06, 09, 12, 15, 18, 21

                        HH for 6hrly - 00, 06, 12, 18

            userip (str): User's IP Address result returned while placing the
                        order for data

            zipFile (str): temporary zip file name created for the data order,
                        returned while placing the order for data

            mailid (str): Mail Id of the user, requesting/placing an order for
                        the CHRS Persiann Data

            data_type (str): Data Collection to be downloaded
                        options:
                            PERSIANN -> PERSIANN,
                            CCS -> PERSIANN-CCS,
                            CDR -> PERSIANN-CDR,
                            PDIR -> PDIR

            compression (str, optional): Download file format.
                        options:
                            zip, 
                            tar (in development)
                        Defaults to 'zip'.

            timestep (str, optional): Time step/interval for the subsequent data
                        files in the time period.
                        options:
                            1hrly,
                            3hrly,
                            6hrly,
                            daily,
                            monthly,
                            yearly,
                        Defaults to 'monthly'.

        Returns:
            file_url (str): url of the file to download If Successful else None
        """

        folder = {
            'PERSIANN': 'PERSIANN',
            'CCS': 'PERSIANN-CCS',
            'CDR': 'PERSIANN-CDR',
            'PDIR': 'PDIR'
        }
        # compress = 'tar.gz' if compression == 'tar' else compression

        gen_url = 'https://chrsdata.eng.uci.edu/php/emailDownload.php'
        dl_base = 'https://chrsdata.eng.uci.edu/userFile'
        file_name = f'{data_type}_{zipFile}.{compression}'
        file_url = f'{dl_base}/{userip}/temp/{folder[data_type]}/{file_name}'

        # gen_url = f'https://chrsdata.eng.uci.edu/php/emailDownload.php?
        # email={mail_id}&downloadLink=https://chrsdata.eng.uci.edu/userFile/
        # {userip}/temp/PERSIANN-CCS/CCS_{zipFile}.zip&fileExtension=zip
        # &dataType=CCS&timestep=monthly&startDate={startmonth}
        # &endDate={endmonth}&domain=wholemap&domain_parameter=undefined'

        dparams = {
            'email': mailid,
            'downloadLink': file_url,
            'fileExtension': compression,
            'dataType': data_type,
            'startDate': start,
            'endDate': end,
            'timestep': timestep,
            'domain': 'wholemap',
            'domain_parameter': 'undefined'
        }

        try:
            gen = requests.get(gen_url, params=dparams)
            if gen.status_code != 200:
                raise Exception('Null Response')
            print(f'File url Generated - {file_url}')
            return file_url
        except Exception:
            return None

    def fetch_data(self, start: str, end: str, mailid: str, data_type: str,
                   download_path: str, file_format: str = 'Tif',
                   timestep: str = 'monthly', compression: str = 'zip'):
        """This function places the order through query and then uses the 
        generate url function to fetch the download url for the file for the 
        PERSIANN, PERSIANN-CCS, PERSIANN-CDR and PDIR data collections. And
        finally, downloads the file to the destination folder.

        Args:
            start (str): start date in 'yyyymmddHH' format
                        HH for 1hrly - 00, 01, ---, 23

                        HH for 3hrly - 00, 03, 06, 09, 12, 15, 18, 21

                        HH for 6hrly - 00, 06, 12, 18

            end (str): end date in 'yyyymmddHH' format
                        HH for 1hrly - 00, 01, ---, 23

                        HH for 3hrly - 00, 03, 06, 09, 12, 15, 18, 21

                        HH for 6hrly - 00, 06, 12, 18

            mailid (str): Mail Id of the user, requesting/placing an order for
                        the CHRS Persiann Data

            data_type (str): Data Collection to be downloaded
                        options:
                            PERSIANN -> PERSIANN,
                            CCS -> PERSIANN-CCS,
                            CDR -> PERSIANN-CDR,
                            PDIR -> PDIR

            download_path (str): local path on the system where the file is
                        downloaded.

            file_format (str, optional): File format for the data to be downloaded.
                        options:
                            ArcGrid,
                            Tif,
                            NetCDF
                        Defaults to 'Tif'.

            timestep (str, optional): Time step/interval for the subsequent data
                        files in the time period.
                        options:
                            1hrly,
                            3hrly,
                            6hrly,
                            daily,
                            monthly,
                            yearly,
                        Defaults to 'monthly'.

            compression (str, optional): Download file format.
                        options:
                            zip, 
                            tar (in development)
                        Defaults to 'zip'.

        Returns:
            (bool): True if Downloaded successfully
        """

        print('Querying data & Placing the order...')
        print(f'''Query Params:

start date - {start}
end date - {end}
time step - {timestep}
data type - {data_type}
file format - {file_format}
compression format - {compression}
download path - {download_path}
''')

        body = self.query_url(start, end, data_type,
                              file_format, timestep, compression)

        if body is None:
            print('Failed to query the data, Try Again.')
            return None

        userip, zipFile = body['userIP'], body['zipFile']

        print('Query complete.')
        print(f'Order Details - User IP: {userip}, File: {zipFile}')

        print('Generating Data url...')
        file_url = self.generate_url(start, end, userip, zipFile,
                                     mailid, data_type, compression, timestep)

        if file_url is None:
            print('Failed to generate download URL, Try Again.')
            return None

        try:
            dpath = Path(download_path).expanduser().absolute()
            filepath = dpath.joinpath(file_url.split('/')[-1])
            print(f'Downloading compressed data file - {filepath}')
            self.download(file_url, filepath)
            print('Download Complete ------------------------------------------\n')
            return True
        except Exception:
            print('Failed to download data file, Try Again.')
            return None

    def get_persiann(self, start: str, end: str, mailid: str, download_path: str,
                     file_format: str = 'Tif', timestep: str = 'monthly',
                     compression: str = 'zip'):
        """This function places the order through query and then uses the 
        generate url function to fetch the download url for the file for
        PERSIANN Data collection. And finally, downloads the file to the 
        destination folder.

        Args:
            start (str): start date in 'yyyymmddHH' format
                        HH for 1hrly - 00, 01, ---, 23

                        HH for 3hrly - 00, 03, 06, 09, 12, 15, 18, 21

                        HH for 6hrly - 00, 06, 12, 18

            end (str): end date in 'yyyymmddHH' format
                        HH for 1hrly - 00, 01, ---, 23

                        HH for 3hrly - 00, 03, 06, 09, 12, 15, 18, 21

                        HH for 6hrly - 00, 06, 12, 18

            mailid (str): Mail Id of the user, requesting/placing an order for
                        the CHRS Persiann Data

            download_path (str): local path on the system where the file is
                        downloaded.

            file_format (str, optional): File format for the data to be downloaded.
                        options:
                            ArcGrid,
                            Tif,
                            NetCDF
                        Defaults to 'Tif'.

            timestep (str, optional): Time step/interval for the subsequent data
                        files in the time period.
                        options:
                            1hrly,
                            3hrly,
                            6hrly,
                            daily,
                            monthly,
                            yearly,
                        Defaults to 'monthly'.

            compression (str, optional): Download file format.
                        options:
                            zip, 
                            tar (in development)
                        Defaults to 'zip'.

        Returns:
            (bool): True if Downloaded successfully
        """

        data_type = 'PERSIANN'

        status = self.fetch_data(start, end, mailid, data_type, download_path,
                                 file_format, timestep, compression)

        return status

    def get_persiann_ccs(self, start: str, end: str, mailid: str, download_path: str,
                         file_format: str = 'Tif', timestep: str = 'monthly',
                         compression: str = 'zip'):
        """This function places the order through query and then uses the 
        generate url function to fetch the download url for the file for
        PERSIANN-CCS Data collection. And finally, downloads the file to the 
        destination folder.

        Args:
            start (str): start date in 'yyyymmddHH' format
                        HH for 1hrly - 00, 01, ---, 23

                        HH for 3hrly - 00, 03, 06, 09, 12, 15, 18, 21

                        HH for 6hrly - 00, 06, 12, 18

            end (str): end date in 'yyyymmddHH' format
                        HH for 1hrly - 00, 01, ---, 23

                        HH for 3hrly - 00, 03, 06, 09, 12, 15, 18, 21

                        HH for 6hrly - 00, 06, 12, 18

            mailid (str): Mail Id of the user, requesting/placing an order for
                        the CHRS Persiann Data

            download_path (str): local path on the system where the file is
                        downloaded.

            file_format (str, optional): File format for the data to be downloaded.
                        options:
                            ArcGrid,
                            Tif,
                            NetCDF
                        Defaults to 'Tif'.

            timestep (str, optional): Time step/interval for the subsequent data
                        files in the time period.
                        options:
                            1hrly,
                            3hrly,
                            6hrly,
                            daily,
                            monthly,
                            yearly,
                        Defaults to 'monthly'.

            compression (str, optional): Download file format.
                        options:
                            zip, 
                            tar (in development)
                        Defaults to 'zip'.

        Returns:
            (bool): True if Downloaded successfully
        """

        data_type = 'CCS'

        status = self.fetch_data(start, end, mailid, data_type, download_path,
                                 file_format, timestep, compression)

        return status

    def get_persiann_cdr(self, start: str, end: str, mailid: str, download_path: str,
                         file_format: str = 'Tif', timestep: str = 'monthly',
                         compression: str = 'zip'):
        """This function places the order through query and then uses the 
        generate url function to fetch the download url for the file for
        PERSIANN-CDR Data collection. And finally, downloads the file to the 
        destination folder.

        Args:
            start (str): start date in 'yyyymmddHH' format
                        HH for 1hrly - 00, 01, ---, 23

                        HH for 3hrly - 00, 03, 06, 09, 12, 15, 18, 21

                        HH for 6hrly - 00, 06, 12, 18

            end (str): end date in 'yyyymmddHH' format
                        HH for 1hrly - 00, 01, ---, 23

                        HH for 3hrly - 00, 03, 06, 09, 12, 15, 18, 21

                        HH for 6hrly - 00, 06, 12, 18

            mailid (str): Mail Id of the user, requesting/placing an order for
                        the CHRS Persiann Data

            download_path (str): local path on the system where the file is
                        downloaded.

            file_format (str, optional): File format for the data to be downloaded.
                        options:
                            ArcGrid,
                            Tif,
                            NetCDF
                        Defaults to 'Tif'.

            timestep (str, optional): Time step/interval for the subsequent data
                        files in the time period.
                        options:
                            1hrly,
                            3hrly,
                            6hrly,
                            daily,
                            monthly,
                            yearly,
                        Defaults to 'monthly'.

            compression (str, optional): Download file format.
                        options:
                            zip, 
                            tar (in development)
                        Defaults to 'zip'.

        Returns:
            (bool): True if Downloaded successfully
        """

        data_type = 'CDR'

        status = self.fetch_data(start, end, mailid, data_type, download_path,
                                 file_format, timestep, compression)

        return status

    def get_pdir(self, start: str, end: str, mailid: str, download_path: str,
                 file_format: str = 'Tif', timestep: str = 'monthly',
                 compression: str = 'zip'):
        """This function places the order through query and then uses the 
        generate url function to fetch the download url for the file for
        PDIR-Now Data collection. And finally, downloads the file to the 
        destination folder.

        Args:
            start (str): start date in 'yyyymmddHH' format
                        HH for 1hrly - 00, 01, ---, 23

                        HH for 3hrly - 00, 03, 06, 09, 12, 15, 18, 21

                        HH for 6hrly - 00, 06, 12, 18

            end (str): end date in 'yyyymmddHH' format
                        HH for 1hrly - 00, 01, ---, 23

                        HH for 3hrly - 00, 03, 06, 09, 12, 15, 18, 21

                        HH for 6hrly - 00, 06, 12, 18

            mailid (str): Mail Id of the user, requesting/placing an order for
                        the CHRS Persiann Data

            download_path (str): local path on the system where the file is
                        downloaded.

            file_format (str, optional): File format for the data to be downloaded.
                        options:
                            ArcGrid,
                            Tif,
                            NetCDF
                        Defaults to 'Tif'.

            timestep (str, optional): Time step/interval for the subsequent data
                        files in the time period.
                        options:
                            1hrly,
                            3hrly,
                            6hrly,
                            daily,
                            monthly,
                            yearly,
                        Defaults to 'monthly'.

            compression (str, optional): Download file format.
                        options:
                            zip, 
                            tar (in development)
                        Defaults to 'zip'.

        Returns:
            (bool): True if Downloaded successfully
        """

        data_type = 'PDIR'

        status = self.fetch_data(start, end, mailid, data_type, download_path,
                                 file_format, timestep, compression)

        return status
