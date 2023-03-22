import aws_cdk as core
import aws_cdk.assertions as assertions

from auto_eip_route53_binding_karpenter.auto_eip_route53_binding_karpenter_stack import AutoEipRoute53BindingKarpenterStack

# example tests. To run these tests, uncomment this file along with the example
# resource in auto_eip_route53_binding_karpenter/auto_eip_route53_binding_karpenter_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AutoEipRoute53BindingKarpenterStack(app, "auto-eip-route53-binding-karpenter")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
