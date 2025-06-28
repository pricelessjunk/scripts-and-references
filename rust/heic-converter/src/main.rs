use std::fs::{File, OpenOptions};

use image::ImageReader;
/// Install vcpkg -> 
/// 
///     git clone https://github.com/microsoft/vcpkg.git
///     cd vcpkg; .\bootstrap-vcpkg.bat
/// 
///     $env:VCPKG_ROOT="C:\path\to\vcpkg"
///     $env:PATH="$env:VCPKG_ROOT;$env:PATH"
/// vcpkg install libheif:x64-windows-static-md
/// cargo vcpkg -v build

use libheif_rs::{
    Channel, RgbChroma, ColorSpace, CompressionFormat,
    EncoderQuality, HeifContext, Image, Result, LibHeif
};

fn main() -> Result<()> {
    let img = ImageReader::open("input.png").unwrap().decode().unwrap().;
    let rgba = img.to_rgb8();
    let (h,w) = rgba.dimensions();

    let lib_heif = LibHeif::new();
    let mut encoder = lib_heif.encoder_for_format(CompressionFormat::Hevc)?;
    encoder.set_quality(EncoderQuality::Lossy(90))?;

    //let mut ctx = HeifContext::read_from_file("input.png")?;
    let mut ctx = HeifContext::new().unwrap();
    //ctx.encode_image(&img, &mut encoder, None);

    let output_path = "output.heic";
    let mut heif_img = 

    ctx.write_to_file(output_path).unwrap();

    //let mut heif_img = Image::new(h, w, ColorSpace::Rgb(rgba))?;


    // Encode image and save it into file.
    // let lib_heif = LibHeif::new();
    // let mut context = HeifContext::new()?;
    // let mut encoder = lib_heif.encoder_for_format(
    //     CompressionFormat::Av1,
    // )?;
    // encoder.set_quality(EncoderQuality::LossLess)?;
    // context.encode_image(&image, &mut encoder, None)?;

    // let tmp_file = NamedTempFile::new().unwrap();
    // context.write_to_file(tmp_file.path().to_str().unwrap())?;

    Ok(())
}