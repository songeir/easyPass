import 'dart:convert';

import 'package:easy_pass/model/user.dart';
import 'package:easy_pass/utils/app_theme.dart';
import 'package:easy_pass/utils/components.dart';
import 'package:easy_pass/utils/function.dart';
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:shared_preferences/shared_preferences.dart';

class LoginPage extends StatefulWidget {
  LoginPage();

  @override
  _LoginPageState createState() => new _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final usernameController = TextEditingController();
  final passwordController = TextEditingController();
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Center(
          child: LayoutBuilder(
            builder: (context, constraints) => Container(
              padding: new EdgeInsets.only(left: 40, right: 40),
              width: (constraints.maxWidth > 400) ? 400 : constraints.maxWidth,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.start,
                children: [
                  SizedBox(height: 80),
                  SvgPicture.asset(
                    'assets/images/logo/easypass-logo-with-text.svg',
                  ),
                  SizedBox(height: 120),
                  MyTextField(
                    hintText: "用户名",
                    restorationId: "username_text_field",
                    controller: usernameController,
                  ),
                  SizedBox(height: 40),
                  MyTextField(
                    hintText: "密码",
                    restorationId: "username_text_field",
                    obscurText: true,
                    controller: passwordController,
                  ),
                  SizedBox(height: 100),
                  // _LoginButton(),
                  MyButton(
                    child: Icon(
                      FontAwesomeIcons.arrowRight,
                      size: 50,
                      color: AppTheme.buildLightTheme().backgroundColor,
                    ),
                    onTap: () {
                      var username = usernameController.text;
                      var password = passwordController.text;

                      _login(context, username, password);
                    },
                  ),
                  Expanded(
                    child: SizedBox(),
                  ),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text('没有账号？'),
                      MaterialButton(
                        child: Text("点此注册"),
                        textColor: Colors.blue,
                        onPressed: () {
                          Navigator.of(context)
                              .pushReplacementNamed('/register');
                        },
                      ),
                    ],
                  ),
                  SizedBox(
                    height: 20,
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

void _login(context, username, password) async {
  var message = await User.login(username, password);

  toast(message);
  if (message == '登陆成功') {
    Navigator.of(context).pushNamedAndRemoveUntil('/home', (route) => false);
  }
}
