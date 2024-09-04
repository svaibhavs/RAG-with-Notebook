# Hands-on Lab: RAG on IBM Power with Sales Manual PDFs

When I did the original lab, we did get it to work, but I was left feeling a little rushed. OK, I had an LLM and RAG running on IBM Power, but what bits did what? Why did I do some of those steps?

So, I set about splitting the work apart, so I could go step by step. And I also wanted to look at a question I get asked a lot, which needs IBM Power specialists like me to go dig into the big documents called Sales Manuals. Could I move the focus of the LLM from Harry Potter to address my work questions, such as "How many processors go into that IBM Power server?"

I therefore have a number of containers here, which are intended to be deployed into the same OCP Project as we used for the earler work. So, we still have the LLM in the Llama CPP Server we used before, and we make use of the Milvus DB we also deployed in the earlier steps.

## 0 Warning!

In the "app.py" files in this section, I have at the moment got hardcoded URLs, which will need to be changes to match the Techzone environment you are using. I hope to change that in the future!

You therefore need to change the URL in this line to match your environment, where "pXXXX" is the environment you are using:

CORS(app, origins=["https://rag-webpage-llm-on-techzone.apps.pXXXX.cecc.ihost.com"]) 

We can work with the Llama CPP Server and Milvus Servers using the connections internal to OCP, so those don't need to be changed, but I could not get the CORS process to work with those internal addresses, as it failed to resolve them.

If you fork your own version of the Git respository, that will allow you to make the changes to the URLs that work for you.

## 1 Deploy the RAG List Collections container

Use the "+Add" option from the lefthand menu to add our first container in this section, importing from Git

![image](../images/OCP-add-from-git.png)

Point OCP at this respository, which I forked from Marvin's orginal work, so put "https://github.com/DSpurway/RAG-with-Notebook" as the URL for the Git Repo. But, don't deploy yet, as we need to go a bit deeper, and work with some of the "advanced Git options"

![image](../images/DIS-RAG-with-notebook.png)

Click "Show advanced Git options". Put "/Part2-RAG-Sales-Manual/RAG-List-Collections" into the "Context dir", and OCP should work out you want to use a Dockerfile. 

![image](../images/context-dir-for-list-collections.png)

I put these containers into a new app, to show them grouped together. So, choose "Create application" in the "Application" pull down menu, then name our app "Sales Manual RAG App". We can use that for the rest of the containers we will deploy. 
Change the name of this deployment to "rag-list-collections" and hit "Create". I am leaving the creation of the route as default, as that allows testing and is also used by the webpage we shall build later. I hope to move to using internal OCP routes in the future, to avoid the issue above!

![image](../images/create-rag-list-collections-1.1.png)

When that container has deployed, we can hit the small icon on the top right of the container icon to open the URL and test the container is working as intended. You are likely to have to accept the security warnings, then, the collections should be listed, which would include "demo" from our ealier work if that is still in place.

![image](../images/test-rag-list-collections.png)

## 2 Deploy the RAG Drop Collections container

With that container deployed and the app created, we can move on to add more. Use the three dots (also called a hamburger) and "Add to application", from Git as we did before. Remember to change the URL on Git so the name resolution works on your environment. 

![image](../images/create-next-container.png)

Again, put "https://github.com/DSpurway/RAG-with-Notebook" as the URL for the Git Repo and open the advanced options. We might want to drop elements from our Vector DB, so put "/Part2-RAG-Sales-Manual/RAG-Drop-Collection" as the context directory to deploy that container. Change the name to "rag-drop-collection" and "Create".

## 3 Deploy the RAG Loader container

Now, we need something load our Sales Manual documents into the Vector DB, so we can repeat the steps above for RAG-Loader. At this point, I have used static versions of the Sales Manual documents for our IBM Power servers based on Power10, pulled down from the Documentation website. As they are not the online versions yet (as I have not worked out how to get through the dynamic HTML that is presently used to access those documents online), changes we announce and make to the Sales Manuals will cause these versions to get out of date. You might therefore want to pull down new copies and put them into Git, if needed. Also, remember to change the URL as before. Put "/Part2-RAG-Sales-Manual/RAG-Loader" in the context directory and name this "rag-loader". 

## 4 Deploy the RAG Get Docs container

As we have a way to load our Sales Manuals into the Vector DB, we will next want to pull back the "chunks" from the documents so we can use them in our prompt to the LLM. Part of the loading process automatically inclused the source document in the metadata that is stored in the Vector DB, so we can get chunks of text back which we know come from the appropriate Sales Manual, and not get mixed up results. Also, we can keep Harry Potter out of this too!

Change the URL before you deploy, then repeat the steps we used before with "/Part2-RAG-Sales-Manual/RAG-Get-Docs" as the context directory and "rag-get-docs" as the name. 

## 5 Deploy the RAG Prompt LLM container

This container is something of a workaround, as it would probably be better if my webpage actually did this step, but I had issues with something called CORS which stopped me doing that. So this container passes the prompt we build over the the LLM. And, as that usually times out on the webpage, we can also come to logs in the pods for this container to actually see the end result! Change the URL as before, then use "/Part2-RAG-Sales-Manual/RAG-Prompt-LLM" as the context directory and "rag-prompt-llm" as the name. 

## 6 Deploy the RAG Webpage container

To pull these all together, I have build a little webpage (which looks less than ideal, but does the job for the moment!). Here, the "app.py" is very basic and does not need changing, but you will have to track down quite a few instances for hardcoded URL to change in the "index.html" file! Sorry about that! You will see I have functions that call out to the containers we just build, so we need to change the URLs (there is one in each) in these five functions:

- myRAG_list_collections_func
- myRAG_drop_collections_func
- myRAG_loader_func
- myRAG_get_docs_func
- myRAG_send_prompt_func

Then we can deploy, using "/Part2-RAG-Sales-Manual/RAG-Webpage" as the context directory and "rag-webpage" as the name. 

You will probably end up with a level of overlap between our applications on the OCP console, so you can drag the application group to a clear space. I also then moved around my deployed containers, as the webpage is at the top and calls the rest. Purely to illistrate how things link together, I use the arrow that appears if you hover over a container to draw arrows from the "rag-webpage" to the other containers. And then from the "rag-prompt-llm" to the original "llama-cpp-server" we had before. 

![image](../images/linking-containers.png)

## 7 Using the RAG Webpage

Open up the URL for our webpage with the small icon as we did earlier with our little test

![image](../images/webpage-service-url.png)

The first time you do this, you hit this security warning, so click "Advanced" and then "Proceed to..." to get passed that. Trust me!

![image](../images/not-private.png)

That should then get to my little webpage. You may notice I left on that Watson Code Assistant was helpful to me doing this work. I am not a developer, and so Python, HTML and JavaScript are all a challenge for me. WCA was therefore useful!

If you click the "Click to List Collections for RAG" button (I have aimed for labels that hopefully are clear on the buttons!), you should see "demo" returned, from the earlier work with Harry Potter. That is the Collection that container the Harry Potter book. 

![image](../images/list-collections-demo.png)

While the existance of that collection actually should not change anything for our Sales Manual work, as we will only call on documents from given sources, you still might like to clean up and drop that collection. You may find that the "Enter a collection above then click to drop that collection" may initially not work. If you go behind the scenes and "Inspect" the webpage, you may see that the page hit a "404" error, which it is actually caused by the "ERR_CERT_AUTHORITY_INVALID" error. That comes from the same security issue we had to get passed to open the webpage. So, if you open up the URLs for our containers manually yourself once, to get passed that warning and proceed, that should sort that issue...

![image](../images/cert-auth-error.png)
