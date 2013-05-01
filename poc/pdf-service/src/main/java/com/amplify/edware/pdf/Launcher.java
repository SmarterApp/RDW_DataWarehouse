package com.amplify.edware.pdf;

import org.springframework.context.support.ClassPathXmlApplicationContext;

/**
 * Hello world!
 *
 */
public class Launcher 
{
    @SuppressWarnings("resource")
	public static void main( String[] args )
    {
    	new ClassPathXmlApplicationContext("application-context.xml");
    }
}
