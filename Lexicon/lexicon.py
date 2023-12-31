commands = {

    '/start': 'Выберите действие для взаимодействие с ботом\n\n\n' 
             '👥 /add_student - Добавляет нового ученика в таблицу clients\n\n'
             '❌ /remove_student - Удаляет ученика из таблицы clients\n\n'
             '🔍 /client_info - Предоставляет полную информацию по имени ученика\n\n'
             '🔍 /all_students - Предоставляет весь список учеников\n\n'
             '📅 /add_lesson - Добавление в таблицу lessons информацию об уроке с учеником\n\n'
             '🗑️ /delete_lesson - По дате, id клиента удаляет информацию об уроке\n\n'
             '💵 /add_payment - Добавить оплату за урок\n\n'
             '💰 /month_payments_student - Предоставляет информацию о сумме оплаты ученика за месяц\n\n'
             '💳 /profit_for_the_day - Предоставляет информацию о сумме прибыли за выбранный день\n\n'
             '💳 /payments_for_month - Сумма платежей учеников за выбранный месяц',
    '/add_students': '👥 Для добавления указать: ФИ, телефон, уровень игры, цель, музыкальный инструмент, заметки если необходимо 👥',
    '/client_info': '🔍 Указать фамилию и имя для получения информации 🔍',
    'add_lesson': '📅 Указать id клиента, дата в формате ДД-ММ-ГГГГ 📅',
    '/full_name_students': '📋 Выведет все имена студентов 📋',
    '/delete_lesson': '🗑️ Удаляет запись об уроке: указать id ученика, дату урока в формате ДД-ММ-ГГГГ 🗑️',
    '/add_payment': '💵 Добавить платеж: указать id клиента, сумма платежа, дата платежа(ДД-ММ-ГГГГ), тип платежа(нал, безнал) 💵',
    '/month_payments_student': '💰 Сумма платежа ученика: указать id ученика, дату в формате (ММ-ГГГГ) 💰',
    '/payments_for_month': '💳 Сумма платежей всех учеников за указанный месяц: Указать дату в формате ММ-ГГГГ 💳'
}