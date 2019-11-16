import java.math.BigInteger;
import java.util.Random;

public class RSABig {

	/**
	 * φを返す。
	 *
	 * @param p でっかい素数p
	 * @param q でっかい素数q
	 * @return (p-1)(q-1)
	 */
	public static BigInteger createPhai(BigInteger p, BigInteger q) {
		return p.subtract(BigInteger.valueOf(1)).multiply(q.subtract(BigInteger.valueOf(1)));
	}

	/**
	 * 公開鍵N
	 *
	 * @param p
	 * @param q
	 * @return p * q
	 */
	public static BigInteger createN(BigInteger p, BigInteger q) {
		return p.multiply(q);
	}

	/**
	 * 公開鍵Eを返す
	 *
	 * @param pp
	 * @return φと互いに素な公開鍵E
	 */
	public static BigInteger createE(BigInteger pp) {
		// dを計算
		BigInteger privateKey = null;
		while (true) {
			privateKey = new BigInteger(pp.bitLength(), new Random());
			if ((privateKey.compareTo(pp) != -1) || (privateKey.gcd(pp).compareTo(BigInteger.ONE) != 0)) {
				continue;
			} else {
				return privateKey;
			}
		}
	}

	/**
	 * 秘密鍵の生成
	 *
	 * @param phai
	 * @param e
	 * @return
	 */
	public static BigInteger createPrivateKey(BigInteger phai, BigInteger e) {
		return e.modInverse(phai);
	}

	/**
	 * 暗号化
	 *
	 * @param message
	 * @param es
	 * @param Ns
	 * @return
	 */
	public static String encrypt(BigInteger message, BigInteger es, BigInteger Ns) {
		return message.modPow(es, Ns).toString();
	}

	// 数値の復号化メソッド
	public static BigInteger decrypt(String cry, BigInteger privateKey, BigInteger N) {
		return new BigInteger(cry).modPow(privateKey, N);
	}

	// アルファベットなどの文字列を数字(BigInteger)に変換
	public static BigInteger changeStringToBigInteger(String s) {
		byte b[] = s.getBytes();
		return new BigInteger(b);
	}

	// 数字(BigInteger)をアルファベットなどの文字列に変換
	public static String changeBigIntegerToString(BigInteger bi) {
		byte b[] = bi.toByteArray();
		return new String(b);
	}

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		String str = "tomcat";
		System.out.println("input = " + str);

		// 秘密鍵のpとqを作成
		BigInteger p = new BigInteger(128, 128, new Random());
		BigInteger q = new BigInteger(128, 128, new Random());
		System.out.println("p = " + p);
		System.out.println("q = " + q);

		BigInteger N = createN(p, q);
		System.out.println("N = " + N);

		BigInteger phai = createPhai(p, q);
		System.out.println("phai = " + phai);

		BigInteger e = createE(phai);
		System.out.println("e = " + e);

		BigInteger privateKey = createPrivateKey(phai, e);
		System.out.println("privateKey = " + privateKey);

		BigInteger message = changeStringToBigInteger(str);
		System.out.println("message = " + message);

		String encrypted = encrypt(message, e, N);
		System.out.println("encrypted = " + encrypted);

		BigInteger decrypted = decrypt(encrypted, privateKey, N);
		System.out.println("decrypted = " + decrypted.toString());

		System.out.println("output = " + changeBigIntegerToString(decrypted));
	}
}