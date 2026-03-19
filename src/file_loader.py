import csv
from typing import List

from network import Mode, Route, Stop, Network


class FileLoader:
    def _load_stops(self, filepath: str) -> List[Stop]:
        """
        从CSV文件加载站点数据
        CSV格式: id,name
        """
        stops = []
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    stop = Stop(
                        id=row['id'].strip(),
                        name=row['name'].strip()
                    )
                    stops.append(stop)
            print(f"成功加载 {len(stops)} 个站点")
        except FileNotFoundError:
            print(f"错误: 找不到文件 {filepath}")
        except Exception as e:
            print(f"加载站点时出错: {e}")
        
        return stops

    def _load_routes(self, filepath: str) -> List[Route]:
        """
        从CSV文件加载路线数据
        CSV格式: start_id,end_id,duration,cost,mode
        """
        routes = []
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    # 先创建临时的Stop对象，后面build_network时会替换
                    start_stop = Stop(row['start_id'].strip(), "")
                    end_stop = Stop(row['end_id'].strip(), "")
                    
                    route = Route(
                        start=start_stop,
                        end=end_stop,
                        duration=float(row['duration']),
                        cost=float(row['cost']),
                        mode=Mode[row['mode']]  # 将字符串转换为Enum
                    )
                    routes.append(route)
            print(f"成功加载 {len(routes)} 条路线")
        except FileNotFoundError:
            print(f"错误: 找不到文件 {filepath}")
        except KeyError as e:
            print(f"CSV文件格式错误: 缺少列 {e}")
        except Exception as e:
            print(f"加载路线时出错: {e}")
        
        return routes
    
    def _validate_network(self, stops: List[Stop], routes: List[Route]) -> bool:
        """
        验证网络数据的完整性
        - 确保所有路线的起点和终点都在站点列表中
        """
        stop_ids = {stop.id for stop in stops}
        for route in routes:
            if route.start.id not in stop_ids:
                print(f"错误: 路线起点 {route.start.id} 不在站点列表中")
                return False
            if route.end.id not in stop_ids:
                print(f"错误: 路线终点 {route.end.id} 不在站点列表中")
                return False
        return True

    def build_network(self, stops_file: str, routes_file: str) -> Network:
        stops: List[Stop] = self._load_stops(stops_file)
        routes: List[Route] = self._load_routes(routes_file)
        if not self._validate_network(stops, routes):
            print("网络数据验证失败")
            return None
        network = Network(stops=stops, routes=routes)
        return network