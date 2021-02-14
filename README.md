
# PyroVision  
  
```text  
      _____             __      ___     _             
     |  __ \            \ \    / (_)   (_)            
     | |__) |   _ _ __ __\ \  / / _ ___ _  ___  _ __  
     |  ___/ | | | '__/ _ \ \/ / | / __| |/ _ \| '_ \ 
     | |   | |_| | | | (_) \  /  | \__ \ | (_) | | | |
     |_|    \__, |_|  \___/ \/   |_|___/_|\___/|_| |_|
             __/ |                                    
            |___/
```  
Infrastructure as Code as a RESTful service, powered by Terraform.  
  
## Features  
  
### Managed Infrastructure as code  
  
**PyroVision** provides a RESTful integration for Terraform, which helps you centrally manage your Infrastructure.  
You can use JSON syntax to specify your regular Terraform resources, while using a hosted API to manage common   
Terraform frustrations, such as keeping a unified version across developers and managing the state file.  
  
### User interface for stack management  
  
On top of this, **PyroVision** has a simple UI, which gives you an overview of the stacks you have deployed,  
and provides easy management for deleting and updating them.  
  
### Power-up using a full programming language  
  
The fact that **PyroVision** is language-agnostic, can help you in powering up your IaC setup.  
Being able to use the tools of a full programming language, allows you to integrate   
your application and its infrastructure more easily. You will also be able to generate repetitive resources,   
create intuitive wrappers for your development teams around the core product or even apply automated checks   
on planned changes before actually committing them.  
  
## Get started  
  
This repository holds a docker-compose file that can be used to set up   
a PyroVision server with needed backend resources. For this example a DynamoDB implementation is used as 'StackStore'  
and the SimpleLocalTerraformClient is used as Terraform backend. Both classes can be interchanged with   
custom implementations. Extend the ABC classes in the `api` package to provide custom implementations.  
  
The command to run is simply:  
```  
docker-compose up  
```  
The server will be running at http://localhost:8080.  
  
The UI will be running at http://localhost:5000.  
  
## Roadmap  
  
Currently, on the roadmap are the following topics  
* Enable more features from the UI, such as deleting and creating stacks  
* Provide a Java SDK and improve the Python SDK  
* Authentication module for the API   
* Extensive unit testing for the API / SDK  
* CI flows to create proper releases  
* Kafka Notification service with examples  
* Implement more Terraform features through the API