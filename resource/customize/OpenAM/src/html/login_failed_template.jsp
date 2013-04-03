<%--
   DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS HEADER.
  
   Copyright (c) 2005 Sun Microsystems Inc. All Rights Reserved
  
   The contents of this file are subject to the terms
   of the Common Development and Distribution License
   (the License). You may not use this file except in
   compliance with the License.
                                                                                
   You can obtain a copy of the License at
   https://opensso.dev.java.net/public/CDDLv1.0.html or
   opensso/legal/CDDLv1.0.txt
   See the License for the specific language governing
   permission and limitations under the License.
                                                                                
   When distributing Covered Code, include this CDDL
   Header Notice in each file and include the License file
   at opensso/legal/CDDLv1.0.txt.
   If applicable, add the following below the CDDL Header,
   with the fields enclosed by brackets [] replaced by
   your own identifying information:
   "Portions Copyrighted [year] [name of copyright owner]"
                                                                                
   $Id: login_failed_template.jsp,v 1.5 2008/08/15 01:05:29 veiming Exp $
                                                                                
--%>
<%--
   Portions Copyrighted 2012 ForgeRock AS
--%>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
    <%@ page import="com.sun.xml.internal.messaging.saaj.util.Base64" %>
    <%@ page import="java.io.ByteArrayOutputStream" %>
    <%@ page import="java.io.IOException" %>
    <%@ page import="java.net.URLDecoder" %>
    <%@ page import="java.util.StringTokenizer" %>
    <%@ page import="java.util.zip.DataFormatException" %>
    <%@ page import="java.util.zip.Inflater" %>
    <%@page info="Authentication Error" language="java"%>
    <%@taglib uri="/WEB-INF/jato.tld" prefix="jato"%>
    <%@taglib uri="/WEB-INF/auth.tld" prefix="auth"%>
    <jato:useViewBean className="com.sun.identity.authentication.UI.LoginViewBean">
        <%@page contentType="text/html" %>
        <head>
            <title><jato:text name="htmlTitle_AuthFailed" /></title>
            <%
                String ServiceURI = (String) viewBean.getDisplayFieldValue(viewBean.SERVICE_URI);
                try {
                    String LoginURL = (String)viewBean.getDisplayFieldValue("LoginURL");
                    if(LoginURL!=null) {
                        // read URL parameters for RelayState
                        StringTokenizer st = new StringTokenizer(LoginURL,"&");
                        while(st.hasMoreTokens()) {
                            String[] token=st.nextToken().split("=");
                            if(token!=null&&token.length==2&&"RelayState".equals(token[0])) {
                            // decode URL
                            String RelayState = URLDecoder.decode(token[1], "UTF-8");
                                // decode Base64
                                Base64 base64=new Base64();
                                byte[] decoded = base64.decode(RelayState.getBytes());
                                // inflate compressed string
                                ByteArrayOutputStream baos = new ByteArrayOutputStream(decoded.length);
                                Inflater inflater=new Inflater(true);
                                inflater.setInput(decoded);
                                byte[] buffer = new byte[1024];
                                while(!inflater.finished()) {
                                    int count = inflater.inflate(buffer);
                                    baos.write(buffer, 0, count);
                                }
                                baos.close();
                                // replate new LoginURL
                                String output = new String(baos.toByteArray());
                                viewBean.setDisplayFieldValue("LoginURL", output);
                            }
                        }
                    }
               } catch(Exception e) {} // if there is any exception, we just use the original LoginURL value.
            %>
            <link href="<%= ServiceURI%>/css/new_style.css" rel="stylesheet" type="text/css" />
            <!--[if IE 9]> <link href="<%= ServiceURI %>/css/ie9.css" rel="stylesheet" type="text/css"> <![endif]-->
            <!--[if lte IE 7]> <link href="<%= ServiceURI %>/css/ie7.css" rel="stylesheet" type="text/css"> <![endif]-->
            <link rel="stylesheet" type="text/css" href="<%= ServiceURI%>/config/auth/opensso/css/bootstrap.min.css" />
            <link href="<%= ServiceURI%>/config/auth/opensso/css/edware.css" rel="stylesheet" type="text/css" />
        </head>
        <body>
            <div class="container_12">
                <div id="header">
                    <div id="logo">LOGO</div>
                </div>
                <div class="clear-float">
                    <div>
                        <div class="clear-float">
                            <div>
                                <h3>Invalid username/password combination. Please re-enter your credentials.</h3>
                                <p>
                                    <jato:content name="ContentStaticWarning">
                                        <jato:getDisplayFieldValue name='StaticTextWarning' defaultValue='' fireDisplayEvents='true' escape='false'/>
                                    </jato:content>
                                </p>
                                <jato:content name="ContentHref">
                                    <p><auth:href name="LoginURL" fireDisplayEvents='true'><jato:text name="txtGotoLoginAfterFail" /></auth:href></p>
                                </jato:content>
                            </div>
                        </div>
                    </div>
                </div>
                <div id="footer"></div>
            </div>
        </body>
    </jato:useViewBean>
</html>
