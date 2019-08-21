package com.learnzpk;

import java.io.IOException;
import java.io.RandomAccessFile;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;

/**
 * @author learnzpk
 * @date 2019/07/25
 * @description FileChannel: 从文件中读写数据
 */
public class TestChannel {
    public void writeText(String path,String text){}

    public static void main(String[] args) throws IOException {
        /* 创建一个随机文件读写数据流*/
        RandomAccessFile file = new RandomAccessFile("/Users/learnzpk/CodeSpace/PzpMoudles/FurtherLearn/learn_nio/src/main/resources/data/nio-data.txt", "rw");
        /* 创建一个通道*/
        FileChannel inChannel = file.getChannel();
        /* 分配48字节大小的缓冲池*/
        ByteBuffer buffer = ByteBuffer.allocate(48);
        /* 从通道中读取数据到Buffer中*/
        int bytesRead = inChannel.read(buffer);
        while (bytesRead != -1) {
            System.out.println("Read " + bytesRead);
            /*反转Buffer: 读写指针指到缓存头部，并且设置了最多只能读出之前写入的数据长度*/
            buffer.flip();
            /*position < limit*/
            while (buffer.hasRemaining()) {
                System.out.print((char) buffer.get());
            }
            buffer.clear();
            bytesRead = inChannel.read(buffer);
        }
    }
}
