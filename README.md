# CS251-PROJECT
**Team members:2100500106-210050052-210050168**

Portal for courses is website which provides services to its users for educational purpose.Some of it's important features include:
## Signup
- This website requires authentication, so When a user visits the home page.If he has no account he should  create an account, then they must use the SignUp option. It redirects us to the **Signup** portal, where user can create an account.
- Here we can choose a username of our interest within 150 characters and also create a password for this username following certain protocols like having atleast 8 characters, not entirely numeric etc for security reasons.Also asks for some personal information includes like email,first_name,last name.And he must select role as student/instructor

## Login
- Once an account is created we can use those credentials to login into our account and on succesful login, We can see the **Instructor/Student Home** page based on their role they used in **Signup**

## Home Page
#### Instructor Home Page
- After we login in to the website we can see navigation bar.
- In navigation bar We have the options of **Editing** our profile and we also have an option for **changing password**. and **logout**
- In body of page we have links to **Create Course** and **View Created Courses**

#### Student Home Page
- After we login in to the website we can see navigation bar which is same as that of the instructor page
- In body of page we have links to **Join Course** and **View Joined Courses** and **Avialable Courses**

## Courses
### Instructor's Role:
Instructor can create course,view created courses,view course
#### Create Course Role:
- When we go to this option we will have a form to create course.Here we can chooses course name,**course code**,image,instructor details,Description about course.
#### View Created Courses
- When we go to this we can see a  block is created for each of course which are created by instructor until then and it has course name,instructorname,course code,has an image(which are uploaded by instructor while creating respective course) .
In each course we have a link to **view course**
#### View Course
- Here we can see all details about this course like instructor name,About Instructor,About Course.
- Also we have a link to create assignments **Create Assignment** and also a link to to view created assignment status **View Created Assignments**
### Student's Role:
Student can join course,view joined courses,view available courses
#### Join Course
- When we go to this it asks for a course code(which is unique for every course) to which you want to join.
#### View Available Course.
- When we go this we can see all courses that are available i.e which are created by all instructors but he will not have any access to view these courses can only see instructor name,course name.When he joins a course with a valid course code that course gets visible on view joined courses which he will have access to view.
#### View Joined Course
- When we go to this we can see a  block is created for each of joined courses and it has course name,instructorname,has an image(which are uploaded by instructor while creating respective course)
- Also we have a link to view assignments **View Assignment** which are created by instructor in that respective course 
## Assignments
### Instructor's Role:
#### Create Assignment
- Here instructor can create an assignment in that course which will be visible for student who joined in that course.He has to fill assignment name,Question Content,related Question File,Max marks for assignment,deadline,
- Also has to choose Valid Extensions for answer file(used for file extension verification for student),File directory structure textfile(used for file directory verification for student) and also autograder_script_file if he chooses to do automatic_grading
#### View Created Assignments
- When we go to this we can see list of blocks for all assignments which are created by instructor in that particular course.
- Each assignment block contains Assignment name,Question content,Related Question File,Max marks,deadline which are filled by instructor at time of creating assignment.
- They also contains link to view all submissions **Submitted Assignments** done by students to that particular assignment.
### Student's Role:
#### View Assignment
- When we go this we can see list of blocks for all assignments which are created by instructor in that particular course.
- In each of it we can see info about assignments like Question file,Question Content,... also valid extensions and valid file directory structure  for submission 
- They also contains link to submit assignment  **Submit Assignment** to that particular assignment
- Once he submitted file links to resubmit assignment **Resubmit Assignment** and view his submitted file **VIEW SUBMISSION** will be generated and a link to view his grade **View Grade**
## Assignment Submission
### Student's Role:
#### Submit Assignment
- Here students can submit their solution to assignment.He has to fill content and attach his answer file with correct extension.He can submit it only before deadline which is given by instructor.But once the deadline has passed he couln't submit. 
- If he submits file which has invalid extension(i.e not mentioned by instructor) then he gets error and he can't upload his submission.
- Similarly he can only upload file which has file directory as meantioned by instructor else it throws him an error and can't upload his submission.
####  Resubmit Assignment
- Once he submitted once he has chance to resubmit until deadline.But once deadline has passed it doesn't work.
- When he goes to this he has to fill form just like he did his first submission.File extension and File directory Structure of Uploading file must be valid  same as that of the previous.Once he succesfully upload his file.The previous submission gets erased.  
#### VIEW SUBMISSION:
- Here he will be able to  see his own submission  for that particular assignment.Whenever student resubmits the assignment the submission gets modified automatically.
### Instructor's Role:
#### Submitted Assignments
- Instructor can see list of blocks for all submissions done by different students for that particualr Assignment until then.
- Note:There will be only 1 submission block corresponding to particular student even though he resubmits,   
the previous submission block will be modified  but no new block will be created.
- In each of block we can see username of student and his answer for that assignment and also has a link for his submitted file.At last there is an option to grade that assignment submission **Grade Assignment Submission** 
## Manual Grade
### Instructor's Role:
#### Grade Assignment Submission
- Once instructor goes to this he has to fill marks(must be leass than max marks for that assignment),feedback for that assignment submission done by a particular student.Once he submits this it will reflect on student's side automatically.He can give grade for a assignment submission only once.
### Student's Role:
#### View Grade
- Student can click link to view manual grade in assignment's page.When he goes there he can see his marks and feedback if it is manually submitted by instructor for his submission.
## Automatic Grade
- If instructor chooses automatic grading for an assignment i.e if he uploads a valid autograder_script(ZIP file) then whenever a student make submission for that assignment,he gets his grade and feedback automatically according to that autograder_script which will be visible when he clicks link "automatic grade".
Note: Autograder script is valid
- It must be zip file,it must contain only one ".sh" file inside it.It restricts the student to submit only tar files with name username_---(.tar/.tgz/.tar.gz) 
