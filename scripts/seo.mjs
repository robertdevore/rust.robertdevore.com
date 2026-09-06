export function structuredData({origin,title,description,url,lesson,lessons}) {
 const person={'@type':'Person','@id':`${origin}/about/#author`,name:'Robert DeVore',url:`${origin}/about/`};
 const website={'@type':'WebSite','@id':`${origin}/#website`,name:'Rust Course',url:`${origin}/`,inLanguage:'en',creator:{'@id':person['@id']}};
 const page={'@type':lesson?['WebPage','LearningResource']:url==='/about/'?'AboutPage':url==='/course/'?'CollectionPage':'WebPage','@id':origin+url+'#webpage',url:origin+url,name:title,description,inLanguage:'en',isPartOf:{'@id':website['@id']},author:{'@id':person['@id']},isAccessibleForFree:true};
 const graph=[person,website,page];
 if(url==='/course/')page.mainEntity={'@id':`${origin}/course/#course`};
 if(url==='/course/')graph.push({'@type':'Course','@id':`${origin}/course/#course`,name:'Practical Rust Course',description,url:origin+url,inLanguage:'en',isAccessibleForFree:true,author:{'@id':person['@id']},hasPart:lessons.map(l=>({'@id':origin+l.url+'#webpage'}))});
 if(lesson){page.learningResourceType='lesson';page.isPartOf=[{'@id':website['@id']},{'@id':`${origin}/course/#course`}];page.timeRequired=`PT${lesson.minutes}M`;page.about={'@type':'Thing',name:'Rust programming language'};page.breadcrumb={'@id':origin+url+'#breadcrumb'};graph.push({'@type':'BreadcrumbList','@id':origin+url+'#breadcrumb',itemListElement:[{name:'Rust Course',item:origin+'/'},{name:'Curriculum',item:origin+'/course/'},{name:title,item:origin+url}].map((x,i)=>({'@type':'ListItem',position:i+1,...x}))});}
 return JSON.stringify({'@context':'https://schema.org','@graph':graph}).replaceAll('<','\\u003c');
}
