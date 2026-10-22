import io
import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps

st.set_page_config(
    page_title="ID-Gen Pro",
    page_icon="🆔",
    layout="wide"
)

st.sidebar.markdown("### ⚙️ Configuración")
nombre = st.sidebar.text_input("Nombre Completo", value="JUAN PEREZ")
cargo = st.sidebar.text_input("Cargo", value="Coordinador")
id_empleado = st.sidebar.text_input("Número de Empleado", value="EMP-0001")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎨 Estética")
color_marca = st.sidebar.color_picker("Color de la Marca", value="#1E40AF")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📷 Multimedia")
archivo_foto = st.sidebar.file_uploader(
    "Subir foto de perfil", 
    type=["jpg", "png", "jpeg"]
)

def generar_carnet(nombre, cargo, id_empleado, color_hex, foto_bytes):
    
    ancho, alto = 400, 600
    
    carnet = Image.new("RGB", (ancho, alto), "#FFFFFF")
    draw = ImageDraw.Draw(carnet)
    

    alto_banner = int(alto * 0.35)
    draw.rectangle([(0, 0), (ancho, alto_banner)], fill=color_hex)
    

    if foto_bytes is not None:
        foto = Image.open(foto_bytes).convert("RGBA")
    else:
        
        foto = Image.new("RGBA", (300, 300), "#CBD5E1")
    
    
    tamano_foto = 180
    foto_cuadrada = ImageOps.fit(foto, (tamano_foto, tamano_foto), Image.Resampling.LANCZOS)
    
   
    mascara = Image.new("L", (tamano_foto, tamano_foto), 0)
    draw_mascara = ImageDraw.Draw(mascara)
    draw_mascara.ellipse((0, 0, tamano_foto, tamano_foto), fill=255)
    
    
    foto_circular = Image.new("RGBA", (tamano_foto, tamano_foto), (0, 0, 0, 0))
    foto_circular.paste(foto_cuadrada, (0, 0), mascara)
    
    
    borde_tamano = tamano_foto + 8
    borde_img = Image.new("RGBA", (borde_tamano, borde_tamano), (0, 0, 0, 0))
    draw_borde = ImageDraw.Draw(borde_img)
    draw_borde.ellipse((0, 0, borde_tamano, borde_tamano), fill="white")
    
    
    pos_x = (ancho - tamano_foto) // 2
    pos_y = alto_banner - (tamano_foto // 2)
    pos_borde_x = (ancho - borde_tamano) // 2
    pos_borde_y = alto_banner - (borde_tamano // 2)
    
    carnet.paste(borde_img, (pos_borde_x, pos_borde_y), borde_img)
    carnet.paste(foto_circular, (pos_x, pos_y), foto_circular)
    
    try:
        font_nombre = ImageFont.truetype("arial.ttf", 22)
        font_cargo = ImageFont.truetype("arial.ttf", 15)
        font_id = ImageFont.truetype("arial.ttf", 14)
        font_pie = ImageFont.truetype("arial.ttf", 11)
    except:
        font_nombre = ImageFont.load_default()
        font_cargo = ImageFont.load_default()
        font_id = ImageFont.load_default()
        font_pie = ImageFont.load_default()

  
    draw.text((ancho/2, pos_y + tamano_foto + 30), nombre.upper(), fill="#0F172A", font=font_nombre, anchor="mm")
    draw.text((ancho/2, pos_y + tamano_foto + 60), cargo.title(), fill="#64748B", font=font_cargo, anchor="mm")
    draw.text((ancho/2, pos_y + tamano_foto + 110), f"EMPLEADO ID: {id_empleado}", fill="#334155", font=font_id, anchor="mm")
    

    draw.rectangle([(0, alto - 40), (ancho, alto)], fill="#F8FAFC")
    draw.text((ancho/2, alto - 20), "PROPIEDAD PRIVADA - USO INTERNO", fill="#94A3B8", font=font_pie, anchor="mm")
    
    return carnet


st.markdown("<h1 style='text-align: center; color: #EF4444;'>🆔 ID-Gen Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94A3B8;'><b>Proyecto Final:</b> Generador de Identidad Corporativa</p>", unsafe_allow_html=True)
st.markdown("---")


col_vista, col_exportar = st.columns([1.2, 1])


imagen_carnet = generar_carnet(nombre, cargo, id_empleado, color_marca, archivo_foto)


buffer = io.BytesIO()
imagen_carnet.save(buffer, format="PNG")
buffer.seek(0)

with col_vista:
    st.subheader("Vista Previa")
    st.image(imagen_carnet, caption="Carnet Generado", use_container_width=True)

with col_exportar:
    st.subheader("Exportar")
    st.write(
        "Verifica que los datos sean correctos. "
        "La imagen se descargará en formato PNG de alta resolución."
    )
    

    st.download_button(
        label="📥 Descargar Credencial",
        data=buffer,
        file_name=f"credencial_{id_empleado.lower()}.png",
        mime="image/png",
        use_container_width=True,
        type="primary"
    )
    
    if st.button("✨ Limpiar Todo", use_container_width=True):
        st.rerun()