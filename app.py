#!/usr/bin/env python3
import aws_cdk as cdk

# for yaml parsing

from auto_eip_route53_binding_karpenter.auto_eip_route53_binding_karpenter_stack import AutoEipRoute53BindingKarpenterStack



app = cdk.App()
AutoEipRoute53BindingKarpenterStack( app, "AutoEipRoute53BindingKarpenterStack")

app.synth()

