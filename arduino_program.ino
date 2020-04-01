// author: enchant97

#include <EEPROM.h>

const int start_pin = 4;
const int drop_pin = 5;
const int flash_pin = 6;
String serial_data;

int settings_addr = 0; // address of first byte for where the settings are
int settings[4] = {0, 1, 200, 0}; // { dropDelay, dropCount, dropDuration, flashdelay }

void setup()
{
    pinMode(start_pin, INPUT_PULLUP);
    pinMode(drop_pin, OUTPUT);
    pinMode(flash_pin, OUTPUT);
    load_eeprom_values();
    Serial.begin(9600);
    while (!Serial){
        // wait for serial port to connect before sending ready message
    }
    Serial.println("ready");
}

void save_to_eeprom()
{
    EEPROM.put(settings_addr, settings);
}

void load_eeprom_values()
{
    EEPROM.get(settings_addr, settings);
}

void trigger_flash()
{
    digitalWrite(flash_pin, HIGH);
    delay(5);
    digitalWrite(flash_pin, LOW);
}

void trigger_drop()
{
    int current_drops = 0;
    while (current_drops != settings[1])
    {
        delay(settings[0]);
        digitalWrite(drop_pin, HIGH);
        delay(settings[2]);
        digitalWrite(drop_pin, LOW);
        current_drops += 1;
    }
    delay(settings[3]);
    trigger_flash();
}

void test_drop()
{
    digitalWrite(drop_pin, HIGH);
    delay(1000);
    digitalWrite(drop_pin, LOW);
}

void loop()
{
    if (digitalRead(start_pin) == LOW)
    {
        trigger_drop();
        delay(250);
    }
    while (Serial.available() > 0)
    {
        char incomingByte = Serial.read();

        if (incomingByte == '\n')
        {
            Serial.println("ok");
            if (serial_data == "TESTDROP")
            {
                test_drop();
            }
            else if (serial_data == "START")
            {
                trigger_drop();
            }
            else if (serial_data == "SAVECURRENT")
            {
                save_to_eeprom();
            }
            else if (serial_data.startsWith("dropdelay="))
            {
                settings[0] = serial_data.substring(serial_data.indexOf("=") + 1).toInt();
            }
            else if (serial_data.startsWith("dropcount="))
            {
                settings[1] = serial_data.substring(serial_data.indexOf("=") + 1).toInt();
            }
            else if (serial_data.startsWith("dropduration="))
            {
                settings[2] = serial_data.substring(serial_data.indexOf("=") + 1).toInt();
            }
            else if (serial_data.startsWith("flashdelay="))
            {
                settings[3] = serial_data.substring(serial_data.indexOf("=") + 1).toInt();
            }
            serial_data = "";
        }
        else
        {
            serial_data += incomingByte;
        }
    }
    delay(10);
}
