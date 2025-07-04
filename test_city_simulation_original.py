import unittest
from io import StringIO
import sys
from CitySimulation import CitySimulation
import time
timestamp = round(time.time(), 0)
class TestCitySimulation(unittest.TestCase):
    test_number = 0
    def setUp(self):
        self.simulation = CitySimulation()

    def run_command_and_assert(self,command, expected_output):
        try:
            output = StringIO()
            sys.stdout = output
            self.simulation.process_command(command)
            sys.stdout = sys.__stdout__
            result_output = output.getvalue()
            TestCitySimulation.test_number +=1
            print(f'# {TestCitySimulation.test_number}\n>{command}\n{result_output.strip()}',end='')
            self.assertIn(expected_output, result_output)
            print(' "Test passsed!"')
        except AssertionError:
            print()
            print("="*40)
            print(' "Test not passsed!"') 
            print("="*40)
            print(f'AssertionError: Expected output\n"{expected_output}"\nnot found in actual output:\n"{result_output.strip()}"')
            follow=input("q: quit, press other key continue...")
            if follow=='q':
                sys.exit(1)


    def test_commands(self):
        print('testing ...')

        # Paciente entra a un hospital
        self.run_command_and_assert('patient add_patient Billy', 'Patient Billy added to the system.')#comprobado
        self.run_command_and_assert('hospital add_hospital Pinto', 'Hospital Pinto added to the system.')#comprobado
        self.run_command_and_assert('patient enter_hospital Billy Pinto',  'Billy entered Pinto')#comprobado
                                   
        # Mostrar pacientes y hospitales
        self.run_command_and_assert('hospital show_all', 'Current Hospital(s):\nPinto')
        self.run_command_and_assert('patient show_all', 'Current Patient(s):\nBilly')

        # patient solicita un appointment
        self.run_command_and_assert('patient request_appointment Billy Pinto 18:00', 'Appointment scheduled for patient Billy at 18:00 in Pinto')#comprobado
        self.run_command_and_assert('patient check_appointment_status Billy Pinto', 'Billy has an appointment scheduled at 18:00 in Pinto.')#comprobado
        self.run_command_and_assert('hospital show_appointments Pinto', 'Appointments for hospital Pinto:\n- Patient: Billy, Time: 18:00')
        self.run_command_and_assert('hospital cancel_appointment Billy Pinto', 'Appointment for patient Billy canceled in Pinto.')#comprobado
        self.run_command_and_assert('patient request_urgent_care Billy Pinto', 'Urgent care requested for patient Billy in Pinto.')#comprobado
        self.run_command_and_assert('hospital add_department Pinto cardio', 'Department cardio added to Pinto.')#comprobado
        self.run_command_and_assert('hospital show_departments Pinto', 'Departments in Pinto:\n- cardio')#comprobado
        self.run_command_and_assert('hospital assign_room Pinto Billy room1', 'Room room1 assigned to patient Billy in Pinto.')#comprobado
        self.run_command_and_assert('hospital show_urgent_queue Pinto', 'Patient: Billy, Timestamp:')#comprobado
        self.run_command_and_assert('hospital perform_surgery Pinto Billy cardio', "Surgery performed on patient Billy in cardio at Pinto.")#comprobado
                                    

        #mostrar pacientes en urgencias      
        self.run_command_and_assert('hospital show_urgent_queue Pinto', f"Urgent care queue for hospital 'Pinto':\n- Patient: Billy, Timestamp: {timestamp}")#comprobado
                                   
        
        # patient sale de un hospital
        self.run_command_and_assert('patient exit_hospital Billy Pinto', 'Billy exited Pinto.')#comprobado
                                    


        # patient intenta salir de un hospital en el que no está
        self.run_command_and_assert('patient exit_hospital Billy Pinto', 'Patient Billy cannot perform this action because not in it.')#comprobado                              
      
        # Añadir doctor y asignar a otro hospital
        self.run_command_and_assert('hospital add_doctor Pinto Pepe', 'Doctor Pepe added to Pinto.')#comprobado
        self.run_command_and_assert('hospital add_hospital PTS', 'Hospital PTS added to the system.')#comprobado
        self.run_command_and_assert('hospital assign_doctor PTS Pepe', 'Doctor Pepe assigned to PTS.')#comprobado
        self.run_command_and_assert('hospital list_doctors Pinto', 'Doctors in Pinto:\n- Pepe')#comprobado
        self.run_command_and_assert('hospital list_doctors PTS', 'Doctors in PTS:\n- Pepe')#comprobado

        # Asignar enfermera a un hospital
        self.run_command_and_assert('hospital add_department Pinto cardio', 'Department cardio added to Pinto.')#comprobado
        self.run_command_and_assert('hospital assign_nurse Pinto Pepita cardio', 'Nurse Pepita assigned to cardio in Pinto.')#comprobado

        # Eliminar patient y hospital        
        self.run_command_and_assert('patient remove_patient Billy', 'Agent Billy removed from the system.')#comprobado
        self.run_command_and_assert('hospital remove_hospital Pinto', 'Agent Pinto removed from the system.')#comprobado
        self.run_command_and_assert('hospital remove_hospital PTS', 'Agent PTS removed from the system.')#comprobado
        

    def test_remove_hospital_with_restrictions(self):
        print('testing remove_hospital with restrictions...')
    
        # Agregar un hospital
        self.run_command_and_assert('hospital add_hospital Pinto', 'Hospital Pinto added to the system.')# comprobado
    
    
        # No se puede eliminar un hospital con citas programadas
        
        self.run_command_and_assert('patient add_patient Billy', 'Patient Billy added to the system.')# comprobado
        self.run_command_and_assert('patient enter_hospital Billy Pinto',  'Billy entered Pinto')# comprobado
        self.run_command_and_assert('patient request_appointment Billy Pinto 18:00', 'Appointment scheduled for patient Billy at 18:00 in Pinto')# comprobado
        self.run_command_and_assert('hospital remove_hospital Pinto',"Cannot remove hospital Pinto because it has active: appointments, patients.") # comprobado  
        self.run_command_and_assert('hospital cancel_appointment Billy Pinto', 'Appointment for patient Billy canceled in Pinto.')#comprobado                           
          
        # No se puede eliminar un hospital con cirugías programadas
        self.run_command_and_assert('patient request_surgery Billy Pinto cardio', 'Surgery requested for patient Billy in cardio at Pinto.') # comprobado
        self.run_command_and_assert('hospital remove_hospital Pinto', "Cannot remove hospital Pinto because it has active: surgery, patients.") # comprobado                                   
        self.run_command_and_assert('hospital perform_surgery Pinto Billy cardio', "Surgery performed on patient Billy in cardio at Pinto.")#comprobado

        # No se puede eliminar un hospital con patients
        self.run_command_and_assert('hospital remove_hospital Pinto',"Cannot remove hospital Pinto because it has active: patients.") #comprobado                                   
        self.run_command_and_assert('patient exit_hospital Billy Pinto',  'Billy exited Pinto.')#comprobado
                                   

        # Intentar eliminar el hospital nuevamente
        self.run_command_and_assert('hospital remove_hospital Pinto', 'Agent Pinto removed from the system.')#comprobado
    
    
    def test_error_handling(self):
        print('testing error handling...')
        # Intentar agregar un paciente que ya existe
        self.run_command_and_assert('patient add_patient Billy', 'Patient Billy added to the system.')
        self.run_command_and_assert('patient add_patient Billy', 'Agent Billy already exists.')# comprobado

        # patient intenta entrar a un hospital inexistente
        self.run_command_and_assert('patient enter_hospital Billy NonExistentHospital', "Error: Hospital 'NonExistentHospital' not found.")# comprobado
                                    

        # patient intenta salir de un hospital inexistente
        self.run_command_and_assert('patient exit_hospital Billy NonExistentHospital', "Patient Billy cannot perform this action because not in it.")# comprobado                                  

        # Añadir y asignar un doctor, y asignar una enfermera a un hospital inexistente
        
        self.run_command_and_assert('hospital add_doctor Pinto Pepe', "Error: Hospital 'Pinto' not found.")# comprobado
        self.run_command_and_assert('hospital assign_doctor PTS Pepe', "Error: Hospital 'PTS' not found.")# comprobado      
        self.run_command_and_assert('hospital assign_nurse PTS Pepita nodepartment', "Error: Hospital 'PTS' not found.")# comprobado      
            

        # patient intenta eliminar un patient inexistente
        self.run_command_and_assert('patient remove_patient NonExistentpatient', "Agent NonExistentpatient not found.")# comprobado
                                    

        # hospital intenta cancelar un appointment para un patient inexistente
        self.run_command_and_assert('hospital add_hospital Pinto', "Hospital Pinto added to the system.")
        self.run_command_and_assert('hospital cancel_appointment Ofelia Pinto', "No appointment found for patient Ofelia in Pinto.")# comprobado
                                    
if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestCitySimulation)
    unittest.TextTestRunner(verbosity=2).run(suite)
