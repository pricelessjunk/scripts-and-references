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
    let img = ImageReader::open("input.png").unwrap().decode().unwrap();
    let rgba = img.to_rgb8();
    let (h,w) = rgba.dimensions();

    let mut image = Image::new(
        w,
        h,
        ColorSpace::Rgb(RgbChroma::C444)
    )?;

    image.create_plane(Channel::R, w, h, 8)?;
    image.create_plane(Channel::G, w, h, 8)?;
    image.create_plane(Channel::B, w, h, 8)?;

    let planes = image.planes_mut();
    let plane_r = planes.r.unwrap();
    let stride = plane_r.stride;

    let data_r = plane_r.data;
    let data_g = planes.g.unwrap().data;
    let data_b = planes.b.unwrap().data;

    for y in 0..h {
        let mut pixel_index = stride * y as usize;
        for x in 0..w {
            let color = ((x * y) as u32).to_le_bytes();
            data_r[pixel_index] = color[0];
            data_g[pixel_index] = color[1];
            data_b[pixel_index] = color[2];
            pixel_index += 1;
        }
    }

    let lib_heif = LibHeif::new();
    let mut encoder = lib_heif.encoder_for_format(CompressionFormat::Hevc).unwrap();
    encoder.set_quality(EncoderQuality::Lossy(90))?;
    let mut context = HeifContext::new()?;
    context.encode_image(&image, &mut encoder, None)?;

    // OpenOptions::new()
    //     .create_new(true)
    //     .write(true)
    //     .append(true)
    //     .open("output.heic")
    //     .unwrap();
    File::create_new("output.heic").unwrap();
    context.write_to_file("output.heic")?;

    //let mut ctx = HeifContext::read_from_file("input.png")?;
    // let mut ctx = HeifContext::new().unwrap();
    //ctx.encode_image(&img, &mut encoder, None);

    // let output_path = "output.heic";

    // ctx.write_to_file(output_path).unwrap();

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