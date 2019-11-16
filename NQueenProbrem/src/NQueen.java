import java.util.ArrayDeque;
import java.util.Deque;

public class EightQueenN {

	private static class Vec {
		private int i;
		private int j;

		Vec(int i, int j) {
			this.i = i;
			this.j = j;
		}

		public int getI() {
			return this.i;
		}

		public int getJ() {
			return this.j;
		}
	}

	public static void main(String[] args) {
		int size = 7;
		Deque<Vec> result;
		for (int i = 0; i < size; i++) {
			result = set(size, new ArrayDeque<Vec>(), 0, i);
			if (result.size() > 0) {
				result.stream().forEach(vec -> printRow(size,vec));
				System.out.println();
			}
		}
	}

	static void printRow(int size, Vec vec) {
		for (int j = 0; j < size; j++) {
			System.out.printf("%s", j == vec.getJ() ? "⬛️" : "◻️");
		}
		System.out.println();
	}

	static Deque<Vec> set(int size, Deque<Vec> vecs, int i, int j) {
		if (j > size - 1) {
			return new ArrayDeque<Vec>();
		} else if (check(size, vecs, i, j)) {
			vecs.push(new Vec(i, j));
			return vecs.size() == size ? vecs : set(size, vecs, i + 1, 0);
		} else {
			if (j == size - 1) {
				Vec tmp = vecs.pop();
				return set(size, vecs, tmp.getI(), tmp.getJ() + 1);
			} else if (vecs.size() > 0) {
				return set(size, vecs, i, j + 1);
			} else {
				return new ArrayDeque<Vec>();
			}
		}
	}

	static boolean check(int size, Deque<Vec> vecs, int i, int j) {
		boolean result = true;

		for (Vec vec : vecs) {
			if (vec.getJ() == j || vec.getI() + vec.getJ() == i + j
					|| vec.getI() - vec.getJ() + size - 1 == i - j + size - 1) {
				result = false;
			}
		}
		return result;
	}
}