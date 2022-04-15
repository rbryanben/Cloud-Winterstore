# Winterstore
Cloud-Hosted NoSQL Database For Storing Files Securely 

<img src="resources/logos/logo.png" width="300px">

# About
Cloud Winterstore is a cloud storage service that provides object storage through a web service 
interface. It is basically S3 buckets with my own modifications.
Instead of securing files using pre-signed URLs, a client can set access control measures for a file 
upon upload, thereby getting rid of the whole concept of buckets.
For a person to view a file they will have to be either authenticated as the owner of the file, owner 
of the project or the key to that file exists in the current authenticated user’s key set. All users 
having individual accounts.

This along with libraries for python and android that can be used on the developers backend and 
frontend. And to prove the service works, I built a movie streaming application called Doozby that 
uses Cloud Winterstore as its storage.

# Console Demo
https://user-images.githubusercontent.com/63599157/163562936-6d86de01-a999-4448-8361-283da2c46634.mp4
