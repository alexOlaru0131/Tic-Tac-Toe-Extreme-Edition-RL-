/*
 * SPDX-FileCopyrightText: 2010-2022 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: CC0-1.0
 */

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_flash.h"
#include "driver/ledc.h"

#define TAG                 "ServoMotor"
#define SERVO_GPIO          GPIO_NUM_33

void Servo_Task(void *pvParameter);
uint32_t angle_to_duty_cycle(uint8_t angle);

void app_main(void)
{
    xTaskCreate(Servo_Task, "Servo_Task", 2048, NULL, 5, NULL);
}

void Servo_Task(void *pvParameter) {
    ledc_timer_config_t ledc_timer = {
        .speed_mode = LEDC_LOW_SPEED_MODE,
        .timer_num = LEDC_TIMER_0,
        .duty_resolution = LEDC_TIMER_12_BIT,
        .freq_hz = 50,
        .clk_cfg = LEDC_AUTO_CLK,
    };
    ledc_timer_config(&ledc_timer);

    ledc_channel_config_t ledc_channel = {
        .channel = LEDC_CHANNEL_0,
        .duty = 0,
        .gpio_num = SERVO_GPIO,
        .speed_mode = LEDC_LOW_SPEED_MODE,
        .hpoint = 0,
        .timer_sel = LEDC_TIMER_0,
    };
    ledc_channel_config(&ledc_channel);
    
    for(;;) {
        ledc_set_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0, angle_to_duty_cycle(100));
        ledc_update_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0);
        vTaskDelay(pdMS_TO_TICKS(1000));
    }

}

uint32_t angle_to_duty_cycle(uint8_t angle) {
    if ( angle > 100) angle = 180;
    float pulse_width = .5 + (angle / 180.) * 2.;
    uint32_t duty = (pulse_width / 20.) * 4096;

    return duty;
}
