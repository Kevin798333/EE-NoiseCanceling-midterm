import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import resample
import winsound

print("The project im creating is the digital noise cancelation system that imports different audio files and filter out and remove other sounds" )
print("I will be bale to get graphs of the audio files and removed different backfround noise and output the final audio file")

song = []
noise = []
mixed = []
filtered = []


while True:
    print("\nChoose an option:")
    print("1. Import song file")
    print("2. Add noise to music")
    print("3. Mix song and noise")
    print("4. Filter noise from song")
    print("5. Graph frequencies")
    print("6. Compute final cancelation file")
   
    choice = input("Enter a choice: 1-6 ")
   
    if choice == "1":
        print("You choose to import songs: The program will let you upload a file")
        song_name = input("Enter name of sample: ")
        rate, data = wavfile.read(song_name)
        song.append((song_name, rate, data))
        print("Song: "+ song_name + " was added to the project.")
    elif choice =="2":
        print("You chose to add noise to a song: The program will let you add some noise")
        noise_name = input("Enter name of noise sample: ")
        rate, data = wavfile.read(noise_name)
        noise.append((noise_name, rate, data))
        print("Noise: "+ noise_name+ " was added to the project")
    elif choice == "3":
        print("You chose to mix: the program will combine the audios")
        if song and noise:
            song_name,rate_s,data_s, = song[-1]
            noise_name,rate_n,data_n = noise[-1]
            if rate_s != rate_n:
                print("Resampling the rates....")
                num_sample = len(data_s)
                data_n = resample(data_n,num_sample)
                rate_n = rate_s
            min_len = min(len(data_s), len(data_n))
            mix_data = data_s[:min_len] + data_n[:min_len]            
           
            mixed.append(("Mix.wav", rate_s, mix_data.astype(data_s.dtype)))
            print("Created a mix: " + song_name + " and "+ noise_name)
        else:
            print("You need atleast 1 noise and 1 song.")
    elif choice == "4":
        print("You chose to filter from song: the program will let you filter out certain noises from song")
        if mixed and noise:
            mix_name, rate_m, mix_data = mixed[-1]
            noise_name,rate_n,noise_data = noise[-1]
            min_len = min(len(mix_data), len(noise_data))
            filtered_data = mix_data[:min_len] - noise_data[:min_len]
            filtered.append(("Filtered.wav ",rate_m, filtered_data.astype(mix_data.dtype)))
            print("Filtered signal created: by removing " +noise_name+ " from "+mix_name)
        else:
            print("You need mixed audios before filtering.")
    elif choice == "5":
        print("You chose to graph frequencies: the program will show you the graph of different frequencies")
        if song:
            song_name, rate, data = song[-1]
            plt.figure(figsize=(10, 4))
            plt.title(song_name)
            plt.plot(data[:5000])
            plt.xlabel("Sample")
            plt.ylabel("Amplitude")
            plt.show()
        elif noise:
            noise_name, rate, data = noise[-1]
            plt.figure(figsize=(10, 4))
            plt.title(noise_name)
            plt.plot(data[:5000])
            plt.xlabel("Sample")
            plt.ylabel("Amplitude")
            plt.show()
        else:
            print("Need to import at least one song or noise to graph.")
    elif choice == "6":
        print("You chose to compute final destination: the program will show you before and after of filtered out file")
        if filtered and mixed:
            filtered_name, rate_f, filtered_data = filtered[-1]
            mixed_name, rate_m, mix_data = mixed[-1]
            output = "Filtered.wav"
            mixed_output = "Mixed.wav"
            wavfile.write(output,rate_f,filtered_data)
            wavfile.write(mixed_output, rate_m, mix_data)
            print(f"Final output saved as {output}")
            print(f"Mixed audio saved as {mixed_output}")
           
            plt.figure(figsize=(10, 6))
            plt.subplot(2, 1, 1)
            plt.title("Original Mixed Audio")
            plt.plot(mix_data[:5000])
            plt.xlabel("Sample")
            plt.ylabel("Amplitude")

            plt.subplot(2, 1, 2)
            plt.title("Filtered Audio")
            plt.plot(filtered_data[:5000])
            plt.xlabel("Sample")
            plt.ylabel("Amplitude")

            plt.tight_layout()
            plt.show()
            while True:
                select = input("Choose between the mixed(1) or filtered(2) to hear the audio or type (0) to exit: ")
                if select == "1":
                    print("Will Playing original (noisy) mix...")
                    winsound.PlaySound(mixed_output, winsound.SND_FILENAME)
                elif select == "2":
                    print("Will now play the output filtered audio...")
                    winsound.PlaySound(output,winsound.SND_FILENAME)
                elif select == "0":
                    print("Exiting to menu...")
                    break
        else:
            print("No filtered file found. You need to run (option 3) for mix and (option 4) for filter.")
    else:
        print("Invalid choice: try to run program again")
       
    cont = input("Would you like to continue? Enter Y for Yes or N for No. ")
    if cont == "N":
        print("Exiting Program.....")
        break