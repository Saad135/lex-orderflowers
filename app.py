#!/usr/bin/env python3

import aws_cdk as cdk

from lex.lex_stack import LexStack


app = cdk.App()
LexStack(app, "lex")

app.synth()
