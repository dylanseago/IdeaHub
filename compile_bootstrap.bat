@echo on
cd bootswatch
call grunt swatch:custom
cd ..
xcopy /Y bootswatch\custom\bootstrap*.css static\css
exit