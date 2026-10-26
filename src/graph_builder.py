"""Модуль для построения и обхода графа зависимостей."""


def parse_test_file(file_path):
    """Читает тестовый файл и преобразует его в словарь смежности."""
    graph = {}
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or ":" not in line:
                continue
            node, deps_str = line.split(":", 1)
            deps = [d.strip() for d in deps_str.split() if d.strip()]
            graph[node.strip()] = deps
    return graph


def should_skip(package, filter_str):
    """Проверяет, нужно ли пропустить пакет из-за фильтра."""
    return filter_str and filter_str in package


def dfs_recursive(graph, node, depth, max_depth, filter_str, visited, graph_out):
    """Рекурсивный обход в глубину (DFS) для построения полного графа."""
    if depth > max_depth or node in visited:
        return
    if should_skip(node, filter_str):
        return

    visited.add(node)
    graph_out[node] = []

    for dep in graph.get(node, []):
        if not should_skip(dep, filter_str):
            graph_out[node].append(dep)
            dfs_recursive(
                graph, dep, depth + 1, max_depth,
                filter_str, visited, graph_out
            )


def build_dependency_graph(source, test_mode, max_depth, filter_str):
    """Строит полный граф зависимостей на основе источника данных."""
    if test_mode:
        raw_graph = parse_test_file(source)
        start_node = list(raw_graph.keys())[0]
    else:
        # Для реального Maven пока берем только прямые (заглушка)
        raw_graph = {source: []}
        start_node = source

    full_graph = {}
    visited = set()
    dfs_recursive(
        raw_graph, start_node, 0, max_depth,
        filter_str, visited, full_graph
    )
    return full_graph, start_node


def get_install_order(graph, start_node):
    """Вычисляет порядок установки через пост-порядок DFS."""
    order = []
    visited = set()

    def dfs(node):
        if node in visited:
            return
        visited.add(node)
        for dep in graph.get(node, []):
            dfs(dep)
        order.append(node)

    dfs(start_node)
    return order