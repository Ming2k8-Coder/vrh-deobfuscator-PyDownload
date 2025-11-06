import subprocess
total = 0
fault = 0
ff = open("Needdownload.log","w")
try:
    with open("Needdownload.txt","r",encoding='utf-8') as f:
        for line in f:
            if not any(char in line for char in "#"):
                total += 1
                print(str(total) + "-Running:" + 'node '+ ' src/index.js ' + line)
                result = subprocess.run('node '+ ' src/index.js ' + line, capture_output = True, shell = True)
                ff.write("---------------------NEW LINK-------------------\n")
                ff.write(line + '\n')
                ff.write("------STDOUT-------\n")
                if (result.stdout == None):
                    print(f'STDout ERROR {line}')
                    ff.write("NO OUTPUT!\n")
                else:
                    ff.write(str(result.stdout) + '\n')
                ff.write("------STDERR-------\n")
                if (result.stderr == None or result.stderr == b''):
                    print(f'OK! {line}')
                    ff.write("No error!\n")
                else:
                    ff.write(str(result.stderr) + '\n')
                    print("-----ERROR!! READ LOGS-----")
                    fault += 1
                ff.write("---------------------END LINK-------------------\n\n\n")
finally:
    ff.close()
    print("DONE!\n" + "Fault/Total:" + str(fault) + '/' + str(total))
#input("Press anykey to exit")
