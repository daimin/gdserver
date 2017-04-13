package test;

import org.apache.commons.codec.binary.Base64;

import java.io.UnsupportedEncodingException;
import java.nio.ByteBuffer;
import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.Key;
import java.security.NoSuchAlgorithmException;
import java.util.Arrays;

import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.KeyGenerator;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;

/**
 * Created by daimin on 16/1/6.
 */
public class SimpleCrypto {
    static final String algorithmStr = "AES/CBC/PKCS5Padding";

    private static final Object TAG = "AES";

    static private KeyGenerator keyGen;

    static private Cipher cipher;

    static boolean isInited = false;

    private static  void init() {
        try {
            /**为指定算法生成一个 KeyGenerator 对象。
             *此类提供（对称）密钥生成器的功能。
             *密钥生成器是使用此类的某个 getInstance 类方法构造的。
             *KeyGenerator 对象可重复使用，也就是说，在生成密钥后，
             *可以重复使用同一 KeyGenerator 对象来生成进一步的密钥。
             *生成密钥的方式有两种：与算法无关的方式，以及特定于算法的方式。
             *两者之间的惟一不同是对象的初始化：
             *与算法无关的初始化
             *所有密钥生成器都具有密钥长度 和随机源 的概念。
             *此 KeyGenerator 类中有一个 init 方法，它可采用这两个通用概念的参数。
             *还有一个只带 keysize 参数的 init 方法，
             *它使用具有最高优先级的提供程序的 SecureRandom 实现作为随机源
             *（如果安装的提供程序都不提供 SecureRandom 实现，则使用系统提供的随机源）。
             *此 KeyGenerator 类还提供一个只带随机源参数的 inti 方法。
             *因为调用上述与算法无关的 init 方法时未指定其他参数，
             *所以由提供程序决定如何处理将与每个密钥相关的特定于算法的参数（如果有）。
             *特定于算法的初始化
             *在已经存在特定于算法的参数集的情况下，
             *有两个具有 AlgorithmParameterSpec 参数的 init 方法。
             *其中一个方法还有一个 SecureRandom 参数，
             *而另一个方法将已安装的高优先级提供程序的 SecureRandom 实现用作随机源
             *（或者作为系统提供的随机源，如果安装的提供程序都不提供 SecureRandom 实现）。
             *如果客户端没有显式地初始化 KeyGenerator（通过调用 init 方法），
             *每个提供程序必须提供（和记录）默认初始化。
             */
            keyGen = KeyGenerator.getInstance("AES");
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        }
        // 初始化此密钥生成器，使其具有确定的密钥长度。
        keyGen.init(128); //128位的AES加密
        try {
            // 生成一个实现指定转换的 Cipher 对象。
            cipher = Cipher.getInstance(algorithmStr);
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        } catch (NoSuchPaddingException e) {
            e.printStackTrace();
        }
        //标识已经初始化过了的字段
        isInited = true;
    }

    private static byte[] genKey() {
        if (!isInited) {
            init();
        }
        //首先 生成一个密钥(SecretKey),
        //然后,通过这个秘钥,返回基本编码格式的密钥，如果此密钥不支持编码，则返回 null。
        return keyGen.generateKey().getEncoded();
    }

    public static byte[] pad16Byte(byte[] src) {
        int ml = src.length % 16;
        int arsize = src.length;
        if(ml > 0){
            arsize = ((src.length / 16) + 1) * 16;
        }
        byte[] nnm = new byte[arsize];
        for (int i = 0; i < arsize; i++){
            if(i < src.length){
                nnm[i] = src[i];
            }else{
                nnm[i] = 0;
            }
        }

        return nnm;
    }

    private static byte[] encrypt(String content, String password) throws InvalidAlgorithmParameterException {
        try {
            byte[] keyStr = getKey(password);
            SecretKeySpec key = new SecretKeySpec(keyStr, "AES");
//            Cipher cipher = Cipher.getInstance(algorithmStr);//algorithmStr
            byte[] ivbuf = new byte[16];
            for(int i = 0; i < ivbuf.length; i++){
                ivbuf[i] = 0;
            }
            IvParameterSpec iv = new IvParameterSpec(ivbuf);
            Cipher cipher = Cipher.getInstance(algorithmStr);
            byte[] byteContent = content.getBytes("utf-8");
            cipher.init(Cipher.ENCRYPT_MODE, key, iv);//   ʼ
            byte[] result = cipher.doFinal(byteContent);
            return result; //
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        } catch (NoSuchPaddingException e) {
            e.printStackTrace();
        } catch (InvalidKeyException e) {
            e.printStackTrace();
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        } catch (IllegalBlockSizeException e) {
            e.printStackTrace();
        } catch (BadPaddingException e) {
            e.printStackTrace();
        }
        return null;
    }

    private static byte[] decrypt(byte[] content, String password)  throws InvalidAlgorithmParameterException{
        try {
//            System.out.println("before decode.content.length = " + content.length);
            byte[] keyStr = getKey(password);
            SecretKeySpec key = new SecretKeySpec(keyStr, "AES");
            byte[] ivbuf = new byte[16];
            for(int i = 0; i < ivbuf.length; i++){
                ivbuf[i] = 0;
            }
            IvParameterSpec iv = new IvParameterSpec(ivbuf);
 
            Cipher cipher = Cipher.getInstance(algorithmStr);
            cipher.init(Cipher.DECRYPT_MODE, key, iv);//   ʼ
//            System.out.println("after decode.content.length = " + content.length);
            byte[] result = cipher.doFinal(content);
            return result; //
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        } catch (NoSuchPaddingException e) {
            e.printStackTrace();
        } catch (InvalidKeyException e) {
            e.printStackTrace();
        } catch (IllegalBlockSizeException e) {
            e.printStackTrace();
        } catch (BadPaddingException e) {
            e.printStackTrace();
        }
        return null;
    }

    private static byte[] getKey(String password) {
        byte[] rByte = null;
        if (password!=null) {
            rByte = password.getBytes();
        }else{
            rByte = new byte[24];
        }
        return rByte;
    }

    /**
     * 将二进制转换成16进制
     * @param buf
     * @return
     */
    public static String parseByte2HexStr(byte buf[]) {
        StringBuffer sb = new StringBuffer();
        for (int i = 0; i < buf.length; i++) {
            String hex = Integer.toHexString(buf[i] & 0xFF);
            if (hex.length() == 1) {
                hex = '0' + hex;
            }
            sb.append(hex.toUpperCase());
        }
        return sb.toString();
    }

    /**
     * 将16进制转换为二进制
     * @param hexStr
     * @return
     */
    public static byte[] parseHexStr2Byte(String hexStr) {
        if (hexStr.length() < 1)
            return null;
        byte[] result = new byte[hexStr.length() / 2];
        for (int i = 0; i < hexStr.length() / 2; i++) {
            int high = Integer.parseInt(hexStr.substring(i * 2, i * 2 + 1), 16);
            int low = Integer.parseInt(hexStr.substring(i * 2 + 1, i * 2 + 2),
                    16);
            result[i] = (byte) (high * 16 + low);
        }
        return result;
    }

    //注意: 这里的password(秘钥必须是16位的)
    private static final String keyBytes = "EY7HLjyHOQr8WV7w";

    /**
     *加密
     */
    public static String encode(String content){
        //加密之后的字节数组,转成16进制的字符串形式输出
        try {
//            return new String(Base64.encode(encrypt(content, keyBytes), Base64.DEFAULT));
            byte[] ebyte = Base64.encodeBase64(encrypt(content, keyBytes));
            if(ebyte != null){
                return new String(ebyte, "utf-8");
            }
        } catch (InvalidAlgorithmParameterException e) {
            e.printStackTrace();
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }

        return "";
    }

    /**
     *解密
     */
    public static String decode(String content){
        //解密之前,先将输入的字符串按照16进制转成二进制的字节数组,作为待解密的内容输入
//        System.out.println("string.decode = " + content);
        byte[] b = null;
        try {
            b = decrypt(Base64.decodeBase64(content), keyBytes);
        } catch (InvalidAlgorithmParameterException e) {
            e.printStackTrace();
        }

        try {
            return new String(b, "utf-8");
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }
        return "";
    }

    public static byte[] pack(byte[] data, int tid){

        byte[] databuf = new byte[1024];
        for(int i = 0; i < databuf.length ; i++){
            databuf[0] = 0;
        }
        ByteBuffer buf = ByteBuffer.wrap(databuf);
        buf.putShort((short)tid);
        Log.i("pack data = ", new String(data) + "");
        Log.i("pack data.length = ", data.length + "");
        buf.putShort((short) data.length);
        buf.put(data);
        return buf.array();
    }

    public static byte[] uppack(byte[] data){

        ByteBuffer buf = ByteBuffer.wrap(data);
        short t = buf.getShort();
        short s = buf.getShort();

        byte[] m = buf.array();
        byte[] nm = Arrays.copyOfRange(m, 4, s + 4);
//        System.out.println("data.size = " + s);

//        for(byte mm : nnm){
//            System.out.print(mm + " ");
//        }
//
//        System.out.println();
//
//        System.out.println("data.length = " + data.length);
//        System.out.println("nm.length = " + nm.length);
//        System.out.println("nnm.length = " + nnm.length);
//
//        Log.i("unpack type = ", t + "");
//        Log.i("unpack data.length = ", s + "");
        return nm;
    }

    //测试用例
    public static void test1(){
        String content = "vlllllabcdefggsdfasdfasdfddddddddddddddddd";
        String pStr = encode(content );
        System.out.println("加密前："+content);
        System.out.println("加密后:" + pStr);

        String postStr = decode(pStr);
        System.out.println("解密后："+ postStr );
    }

    public static void test2(){
        String s = "hello";
        String es = Base64.encodeBase64String(s.getBytes());
        System.out.println(es);
    }

    public static void test_pad16Byte(){
        byte [] b = new byte[]{
           1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,
           1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,
           1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
        };
        byte[] nb = pad16Byte(b);

        for(byte nbnb : nb){
            System.out.print(nbnb + " ");
        }

        System.out.println();
        System.out.println("length = " + nb.length);
    }

    public static void main(String[] args) {
//        test2();
//        byte[] kb = genKey();
//        System.out.println(parseByte2HexStr(kb));
//        test1();
//        test_pad16Byte();
//        byte [] cbuf = new byte[1024];
//        for(byte nbnb : cbuf){
//            System.out.print(nbnb + " ");
//        }

        System.out.println(encode("123"));
    }
}
