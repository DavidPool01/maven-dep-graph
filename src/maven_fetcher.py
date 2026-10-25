"""Модуль для загрузки и парсинга POM-файлов из Maven."""
import urllib.request
import xml.etree.ElementTree as ET


def build_pom_url(repo_url, group_id, artifact_id, version):
    """Формирует URL к файлу pom.xml на основе координат пакета."""
    group_path = group_id.replace(".", "/")
    base = repo_url.rstrip("/")
    filename = f"{artifact_id}-{version}.pom"
    return f"{base}/{group_path}/{artifact_id}/{version}/{filename}"


def fetch_xml(url):
    """Загружает XML-контент по указанному URL."""
    try:
        with urllib.request.urlopen(url) as response:
            return response.read()
    except Exception as e:
        print(f"Ошибка загрузки URL {url}: {e}")
        return None


def strip_namespaces(root):
    """Удаляет префиксы пространств имен XML для упрощения поиска."""
    for elem in root.iter():
        if '}' in elem.tag:
            elem.tag = elem.tag.split('}')[-1]


def parse_dependencies(xml_content):
    """Извлекает список прямых зависимостей из содержимого POM."""
    root = ET.fromstring(xml_content)
    strip_namespaces(root)

    deps = []
    deps_tag = root.find("dependencies")
    if deps_tag is None:
        return deps

    for dep in deps_tag.findall("dependency"):
        g_id = dep.findtext("groupId", "")
        a_id = dep.findtext("artifactId", "")
        if g_id and a_id:
            deps.append(f"{g_id}:{a_id}")
    return deps


def get_direct_dependencies(repo_url, package, version):
    """Основная функция получения прямых зависимостей пакета."""
    group_id, artifact_id = package.split(":")
    url = build_pom_url(repo_url, group_id, artifact_id, version)
    print(f"Загрузка POM с адреса: {url}")

    xml_content = fetch_xml(url)
    if xml_content is None:
        return []

    return parse_dependencies(xml_content)