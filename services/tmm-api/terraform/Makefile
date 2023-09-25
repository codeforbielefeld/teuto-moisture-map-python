ENV ?= dev

.PHONY: plan apply init clean 


plan: tfplan 

tfplan: *.tf *.tfvars .terraform.lock.hcl
	terraform workspace select $(ENV) && \
	terraform plan -var-file terraform.$(ENV).tfvars -out tfplan


apply: tfplan
	terraform workspace select $(ENV) && \
	terraform apply tfplan

init:
	terraform init

clean:
	rm -rf tfplan