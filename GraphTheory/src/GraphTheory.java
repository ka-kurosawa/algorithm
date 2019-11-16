import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * テンプレートエンジン中の閉路を探索
 */
public class GraphTheory {
	/**
	 * mapから有向隣接行列を作成するメソッド
	 *
	 * @param map
	 *            テンプレート一覧を保持するmapクラス
	 * @return 有向隣接行列
	 */
	private static String[][] makeMatrix(Map<String, String> map) {
		String[][] matrix = new String[map.size()][map.size()];
		List<String> keyslist = new ArrayList<String>(map.size());
		for (Map.Entry<String, String> e : map.entrySet()) {
			keyslist.add(e.getKey());
		}
		String[] keys = (String[]) keyslist
				.toArray(new String[keyslist.size()]);
		int i = 0;
		for (Map.Entry<String, String> e : map.entrySet()) {
			String value = e.getValue().replace("${", "");
			value = value.replace("}", "");
			for (int j = 0; j < matrix[i].length; j++) {
				if (keys[j].equals(value)) {
					matrix[i][j] = "1";
				} else {
					matrix[i][j] = "0";
				}
			}
			i++;
		}
		return matrix;
	}

	/**
	 * 有向隣接行列を冪乗し、対角成分を監視することで閉路を探索
	 *
	 * @param map
	 *            テンプレート一覧を保持するmapクラス
	 * @return 閉路の一部であれば１、違えば０が格納された配列（配列の要素番号はmapの要素番号と一致する）
	 */
	private static int[] powerMatrix(final Map<String, String> map) {
		String[][] matrix = makeMatrix(map);
		String[][] temp = new String[matrix.length][matrix.length];
		String[][] result = new String[matrix.length][matrix.length];
		for (int i = 0; i < matrix.length; i++) {
			for (int j = 0; j < matrix[i].length; j++) {
				result[i][j] = matrix[i][j];
			}
		}
		int[] isCercuit = new int[result.length];
		int res;
		for (int i = 1; i < map.size(); i++) {
			for (int j = 0; j < result.length; j++) {
				for (int k = 0; k < result[j].length; k++) {
					temp[j][k] = result[j][k];
				}
			}
			for (int j = 0; j < matrix.length; j++) {
				for (int k = 0; k < matrix[j].length; k++) {
					res = 0;
					for (int l = 0; l < matrix[j].length; l++) {
						res += Integer.parseInt(temp[j][l])
								* Integer.parseInt(matrix[l][k]);
					}
					result[j][k] = String.valueOf(res);
				}
			}

			for (int j = 0; j < result.length; j++) {
				if ("1".equals(result[j][j])) {
					isCercuit[j] = 1;
				}
			}
		}

		for (int i = 0; i < result.length; i++) {
			for (int j = 0; j < result[i].length; j++) {
				System.out.print(result[i][j] + " ");
			}
			System.out.println();
		}
		return isCercuit;
	}

	/**
	 * 与えられたmapから閉路を除去するメソッド
	 *
	 * @param map
	 *            テンプレート一覧を保持するmapクラス
	 * @return 閉路を構成する成分が全て除去されたmap
	 */

	public static Map<String, String> removeCircuit(Map<String, String> map) {
		List<String> keyslist = new ArrayList<String>(map.size());
		for (Map.Entry<String, String> e : map.entrySet()) {
			keyslist.add(e.getKey());
		}
		String[] keys = (String[]) keyslist
				.toArray(new String[keyslist.size()]);
		int[] isCircuit = powerMatrix(map);
		Map<String, String> resultmap = new LinkedHashMap<String, String>();
		for (int i = 0; i < isCircuit.length; i++) {
			if (isCircuit[i] == 0) {
				resultmap.put(keys[i], map.get(keys[i]));
			}
		}
		return resultmap;
	}

	public static void main(String[] args) {
		Map<String, String> map = new LinkedHashMap<String, String>();

		map.put("test1", "${test2}");
		map.put("test2", "${test3}");
		map.put("test3", "${test4}");
		map.put("test4", "${test5}");
		map.put("test5", "${test6}");
		map.put("test6", "${test7}");
		map.put("test7", "${test8}");
		map.put("test8", "${test2}");

		map = removeCircuit(map);
		for (Map.Entry<String, String> e : map.entrySet()) {
			System.out.println(e.getKey() + " : " + e.getValue());
		}
	}
}
