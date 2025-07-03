from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from replit.object_storage import Client
import os
from keep_alive import keep_alive
keep_alive()

# Initialize Object Storage client
storage_client = Client()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Greeting message
    greeting = (
        "Hello, 2nd Year Prepa Student.\n\n"
        "You will receive a list of essential software tools to assist you in your studies.\n"
        "Please follow the provided links for installation and usage.\n\n"
        "If you face any problems, feel free to contact @Bowling_The_Ripper.\n\n"
        "Now choose your department to access relevant files:"
    )

    # Create main category keyboard (with average grade calculator)
    keyboard = [
        [InlineKeyboardButton("💻 Computer Science 4", callback_data='cs4_menu')],
        [InlineKeyboardButton("🔧 Engineering 1 & RDM", callback_data='eng1_menu')],
        [InlineKeyboardButton("⚙️ Engineering 2", callback_data='eng2_menu')],
        [InlineKeyboardButton("📊 Calculating Average Grade", callback_data='calc_avg_grade')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(greeting, reply_markup=reply_markup)

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        file = await update.message.document.get_file()
        file_path = f"temp_{update.message.document.file_name}"
        await file.download_to_drive(file_path)
        with open(file_path, 'rb') as f:
            storage_client.upload_from_file(update.message.document.file_name, f)
        os.remove(file_path)
        await update.message.reply_text(f"File '{update.message.document.file_name}' uploaded successfully!")
    except Exception as e:
        await update.message.reply_text(f"Error uploading file: {str(e)}")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'cs4_menu':
        await show_cs4_menu(query)
    elif query.data == 'eng1_menu':
        await show_eng1_menu(query)
    elif query.data == 'eng2_menu':
        await show_eng2_menu(query)
    elif query.data == 'back_to_main':
        await show_main_menu(query)
    elif query.data == 'cs4_sql':
        await send_sample_file(query, "cs4_sql_guide.pdf", "🗄️ Computer Science 4 - SQL Study Guide")
    elif query.data == 'eng1_solidworks':
        await send_sample_file(query, "eng1_solidworks_tutorial.pdf", "🔧 Engineering 1 & RDM - SolidWorks Tutorial")
    elif query.data == 'eng2_automgen':
        await send_large_file(query, "eng2_automgen_software.exe", "⚙️ Engineering 2 - Automgen Software (150MB)")
    elif query.data == 'eng2_automgen_link':
        await send_automgen_link(query)
    elif query.data == 'calc_avg_grade':
        await send_average_grade_link(query)

async def send_large_file(query, filename, message):
    try:
        files = storage_client.list()
        if filename in files:
            await query.message.reply_text(
                f"{message}\n\n"
                f"📅 File: {filename}\n"
                f"💾 This is a large file. Click below to start download.\n\n"
                f"⚠️ Note: Large files may take time to download depending on your connection."
            )
            file_data = storage_client.download_as_bytes(filename)
            await query.message.reply_document(document=file_data, filename=filename, caption=f"📁 {filename}")
        else:
            await query.message.reply_text(f"❌ {filename} is not available yet.\nPlease contact admin to upload the file.")
    except Exception as e:
        await query.message.reply_text(f"❌ Error retrieving file: {str(e)}")

async def send_sample_file(query, filename, message):
    try:
        files = storage_client.list()
        if filename in files:
            file_data = storage_client.download_as_bytes(filename)
            await query.message.reply_document(document=file_data, filename=filename, caption=message)
        else:
            sample_content = create_sample_file(filename)
            if sample_content:
                storage_client.upload_from_bytes(filename, sample_content)
                await query.message.reply_document(document=sample_content, filename=filename, caption=message)
            else:
                await query.message.reply_text(f"❌ Sorry, {filename} is not available yet.")
    except Exception as e:
        await query.message.reply_text(f"❌ Error retrieving file: {str(e)}")

def create_sample_file(filename):
    if filename == "cs4_sql_guide.pdf":
        return b"Computer Science 4 - SQL Study Guide\n\nSQL Fundamentals:\n1. SELECT Statements\n2. JOIN Operations\n3. Subqueries\n4. Database Design\n5. Normalization\n6. Indexing"
    elif filename == "eng1_solidworks_tutorial.pdf":
        return b"Engineering 1 & RDM - SolidWorks Tutorial\n\n1. Interface Overview\n2. Sketching Fundamentals\n3. 3D Modeling\n4. Assembly Design\n5. Drawing Creation\n6. Simulation Basics"
    elif filename == "eng2_automgen_manual.pdf":
        return b"Engineering 2 - Automgen Manual\n\n1. PLC Programming Basics\n2. Ladder Logic\n3. Function Blocks\n4. HMI Design\n5. Industrial Automation\n6. Control Systems"
    return None

async def show_cs4_menu(query):
    keyboard = [
        [InlineKeyboardButton("🗄️ SQL", callback_data='cs4_sql')],
        [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='back_to_main')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("💻 Computer Science 4 Files\n\nSelect the file you need:", reply_markup=reply_markup)

async def show_eng1_menu(query):
    keyboard = [
        [InlineKeyboardButton("🔧 SolidWorks", callback_data='eng1_solidworks')],
        [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='back_to_main')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("🔧 Engineering 1 & RDM Files\n\nSelect the file you need:", reply_markup=reply_markup)

async def show_eng2_menu(query):
    keyboard = [
        [InlineKeyboardButton("⚙️ Automgen v8.9 Download", callback_data='eng2_automgen_link')],
        [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='back_to_main')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("⚙️ Engineering 2 Files\n\nSelect the file you need:", reply_markup=reply_markup)

async def show_main_menu(query):
    await start(query, None)

async def send_automgen_link(query):
    try:
        link_message = (
            "⚙️ Automgen v8.9 Software\n\n"
            "📥 Click the link below to download Automgen v8.9:\n\n"
            "🔗 Download Link:\n"
            "https://shivam.dsrbotzz.workers.dev/45795/Automgen_v8.9.rar?hash=AgADtB\n\n"
            "📋 File Info:\n"
            "• Version: 8.9\n"
            "• Format: RAR Archive\n"
            "• Use: PLC Programming & Industrial Automation\n\n"
            "⚠️ Note: This is a direct download link. Make sure you have a good internet connection for downloading."
        )
        await query.message.reply_text(link_message)
    except Exception as e:
        await query.message.reply_text(f"❌ Error sending link: {str(e)}")

async def send_average_grade_link(query):
    try:
        link_message = (
            "📊 Calculate Your Average Grade\n\n"
            "Use this tool to estimate your average grade for CPST2 level:\n\n"
            "🔗 https://okbacalc.byethost9.com/index.html?level=CPST2&i=1"
        )
        await query.message.reply_text(link_message)
    except Exception as e:
        await query.message.reply_text(f"❌ Error sending average grade link: {str(e)}")

app = ApplicationBuilder().token("7706666316:AAE8uhTqMXr3KQSeh8iIW7uysHugJBRY2I4").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_callback))
app.add_handler(MessageHandler(filters.Document.ALL, handle_document))

app.run_polling()