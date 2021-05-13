# Winterstore
Cloud-Hosted NoSQL Database For Storing Files Securely 

# Why Winterstore 
One thing to note is that I am a very big fan of google firebase (https://firebase.google.com/), my favorite part being the fact that it is 
free to use : ) However there are other factors like its very easy to use, hence you do not need to know a lot about backend to build an entire 
application. Which I have done so by building 2 of my applications on it, Solve it (https://github.com/rbryanben/Solve-It) and ChatSock 
(https://github.com/rbryanben/ChatSock-v1.0.2). Bad choice to use Firebase with a C# application btw !

Cutting straight to business, I mostly use Firebase Auth,RTD and Storage for my applications, and 1 thing I have noticed is that they offer the least
security possible when it comes to files. Files are created with a n char long string so that a person may not easily guess the path of the file, but as long as
the person is authenticated they can view any file you created, they just have to guess the url lol.

So my goal is to remake a service like firestore, but this time be a little bit better than the engineers at Google and add  secure access control for sakes.
Fingers crossed on finding someone who will use my code base, but right now its meant for my dissertation


