import data_manage as dm
import trak_utils as tu

def main():
  print(" ==== SoloTrakk ====")
  print(" ==== Din ka Hisab for Lazy Legends. ====")
  print(" ==== HOURLY TRACKER MENU ====")
  print("1. Log new entry")
  print("2. View today's summary")
  print("3. View last 5 logs")
  print("4. Edit")
  print("5. Streaks")
  print("6. Plot")
  print("7. Quit")
  choice = input("Entr choice")
  print("_____________________________________________________________________________________________________________")

  if choice == "1":
    dm.trak()
  elif choice == "2":
    dm.view_today_summary()
  elif choice == "3":
    dm.view_last_logs()
  elif choice == "4":
    dm.edit_entry()
  elif choice == "5":
    tu.view_streak() 
  elif choice == "6":
    tu.plot_weekly_act()
  elif choice == "7":
    break
  
  else:
    print("Invalid choice. Please try again.")

if __name__ == "__main__":
  main()