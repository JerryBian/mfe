import os
import datetime
import xml.etree.ElementTree as ET

from package.sqlpackage import SqlPackage
from package.sqlpackagesetting import SqlPackageSetting


class SqlPackageParserException(Exception):
    pass


class SqlPackageParser(object):

    @staticmethod
    def parse(root: str) -> SqlPackage:
        if not os.path.exists(root):
            raise SqlPackageParserException(
                f'package root {root} does not exists.')

        setting_xml = os.path.join(root, 'setting.xml')
        if not os.path.exists(setting_xml):
            raise SqlPackageParserException(
                f'package setting {setting_xml} does not exists.')

        setting: SqlPackageSetting = __class__.__parse_setting(setting_xml)
        package_root = None
        if setting.date_lookup == 'today':
            package_root = __class__.__get_today_package(root)
        elif setting.date_lookup == 'latest':
            package_root = __class__.__get_latest_package(root)
        else:
            package_root = __class__.__get_today_package(root)
            if not os.path.exists(package_root):
                package_root = __class__.__get_latest_package(root)
        if not os.path.exists(package_root):
            raise SqlPackageParserException(
                f'cannot locate package {package_root}.')

        package: SqlPackage = __class__.__parse_package(package_root, setting)
        return package

    @staticmethod
    def __parse_setting(setting_xml: str) -> SqlPackageSetting:
        tree = ET.parse(setting_xml)
        root = tree.getroot()

        host = root.find('host')
        if host == None:
            raise SqlPackageParserException('cannot find "host" in setting.')

        user = root.find('user')
        if user == None:
            raise SqlPackageParserException('cannot find "user" in setting.')

        password = root.find('password')
        if password == None:
            raise SqlPackageParserException(
                'cannot find "password" in setting.')

        setting = SqlPackageSetting()
        setting.host = host.text
        setting.user = user.text
        setting.password = password.text

        date_lookup = root.find('date-lookup')
        if date_lookup != None:
            setting.date_lookup = date_lookup.text
        return setting

    @staticmethod
    def __parse_package(package_root: str, setting: SqlPackageSetting) -> SqlPackage:
        package_xml = os.path.join(package_root, 'package.xml')
        if not os.path.exists(package_xml):
            raise SqlPackageParserException(
                f'package xml {package_xml} does not exists.')

        tree = ET.parse(package_xml)
        root = tree.getroot()

        result = SqlPackage(setting)
        if 'database' in root.attrib:
            result.database = root.attrib('database').text

        if 'silent' in root.attrib:
            result.silent = bool(root.attrib('silent').text)

        for script in root.iter('script'):
            path = os.path.join(package_root, script.attrib['name'])
            if not os.path.exists(path):
                raise SqlPackageParserException(
                    f'script {path} doesn\'t exist.')
            result.files.append(path)

        return result

    @staticmethod
    def __get_sorted_packages(root):
        package_paths = []
        for p in os.listdir(root):
            full_path = os.path.join(root, p)
            if os.path.isdir(full_path):
                package_paths.append(full_path)

        return sorted(package_paths, key=lambda x: x, reverse=True)

    @staticmethod
    def __get_today_package(root):
        return os.path.join(root, datetime.datetime.utcnow().strftime('%Y%m%d'))

    @staticmethod
    def __get_latest_package(root):
        return __class__.__get_sorted_packages(root)[0]
