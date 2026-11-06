We are working on the final release of the website. This step
incorporate text changes from the new curadoria text. Use your AsUserInput() and group questions. We work in planning first (spec, plan, task, validation) and only implement later.

First, check branchs to see if there is any work in progress. If there is, We finish before reading the rest of this prompt.

We need to:
-imrpove the header/banner visual (using https://unsplash.com/pt-br/fotografias/crianca-segurando-aberto-um-livro-colorido-com-ilustracoes-wccs6fKUtok with proper credits in website)
-the introduction section should incorporate
-incorporate / update texts
-identify missing texts and errors
--for missing text, propose one (use similar ones as reference)
--for mistakes, show me and propose corrections
-Verify text claims agains our data
--pay attention to core concepts and consistency (we sometimes use 0 a 6 anos, sometimes 0 a 5, sometimes 72 meses... we need to be cautious).
-Do a final review of our pipelines and documentation
-Remove the beta bar on top
-we do a full website test for desktop and mobile
-in the introduction section, I want to add a Rio de Janeiro map with the neighboors visible and other demarcations (RA/AP) as a reference of the city geography
-check if footer contains all needed informations (links etc)



For the final report:
-We update it in the website with current text
-We improve its cover and innercover
-We create new editable tex files (1 per chapter) that will replace the report in the next editions
-from now one we edit the report directly as tex file

Also
-curadoria texts should be website only
-we migrate everything to json and similar formats, instead of using the doc

Should we:
-prepare a release for the report in github?
-automate the github actions? (fix errors and dependencies)
---



at the end we change the release from staging\_main into main and ammend the constitution. staging\_main is our test environment, main is the published website.

