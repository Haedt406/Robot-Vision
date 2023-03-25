/*
 *Hunter Lloyd
 * Copyrite.......I wrote, ask permission if you want to use it outside of class. 
 */

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.File;
import java.awt.image.PixelGrabber;
import java.awt.image.MemoryImageSource;
import java.util.prefs.Preferences;
import java.awt.image.BufferedImage;

class IMP implements MouseListener{
   JFrame frame;
   JPanel mp;
   JButton start;
   JScrollPane scroll;
   JMenuItem openItem, exitItem, resetItem;
   Toolkit toolkit;
   File pic;
   ImageIcon img;
   int colorX, colorY;
   int [] pixels;
   int [] results;
   //Instance Fields you will be using below
   //This will be your height and width of your 2d array
   int height=0, width=0;
   //your 2D array of pixels
    int picture[][];
    int original[][];
    int originalHeight = 0;
    int originalWidth = 0;
     MyPanel redPanel;
    MyPanel greenPanel;
    MyPanel bluePanel;
    BufferedImage grid;
    Graphics2D gc;
    /* 
     * In the Constructor I set up the GUI, the frame the menus. The open pulldown 
     * menu is how you will open an image to manipulate. 
     */
   IMP()
   {
      toolkit = Toolkit.getDefaultToolkit();
      frame = new JFrame("Image Processing Software by Hunter");
      JMenuBar bar = new JMenuBar();
      JMenu file = new JMenu("File");
      JMenu functions = getFunctions();
      frame.addWindowListener(new WindowAdapter(){
            @Override
              public void windowClosing(WindowEvent ev){quit();}
            });
      openItem = new JMenuItem("Open");
      openItem.addActionListener(new ActionListener(){
            @Override
          public void actionPerformed(ActionEvent evt){ handleOpen(); }
           });
      resetItem = new JMenuItem("Reset");
      resetItem.addActionListener(new ActionListener(){
            @Override
          public void actionPerformed(ActionEvent evt){ reset(); }
           });     
      exitItem = new JMenuItem("Exit");
      exitItem.addActionListener(new ActionListener(){
            @Override
          public void actionPerformed(ActionEvent evt){ quit(); }
           });
      file.add(openItem);
      file.add(resetItem);
      file.add(exitItem);
      bar.add(file);
      bar.add(functions);
      frame.setSize(600, 600);
      mp = new JPanel();
      mp.setBackground(new Color(0, 0, 0));
      scroll = new JScrollPane(mp);
      frame.getContentPane().add(scroll, BorderLayout.CENTER);
      JPanel butPanel = new JPanel();
      butPanel.setBackground(Color.black);
      start = new JButton("start");
      start.setEnabled(false);
      start.addActionListener(new ActionListener(){
            @Override
          public void actionPerformed(ActionEvent evt){ fun1(); }
           });
      start.addActionListener(new ActionListener(){
            @Override
          public void actionPerformed(ActionEvent evt){ Rotate_90(); }
           });
      start.addActionListener(new ActionListener(){
            @Override
          public void actionPerformed(ActionEvent evt){ grayScale(); }
           });
      start.addActionListener(new ActionListener(){
            @Override
          public void actionPerformed(ActionEvent evt){ blur(); }
           });
      butPanel.add(start);
      frame.getContentPane().add(butPanel, BorderLayout.SOUTH);
      frame.setJMenuBar(bar);
      frame.setVisible(true);}
   /* 
    * This method creates the pulldown menu and sets up listeners to selection of the menu choices. If the listeners are activated they call the methods 
    * for handling the choice, fun1, fun2, fun3, fun4, etc. etc. 
    */
  private JMenu getFunctions(){
     JMenu fun = new JMenu("Functions");
     JMenuItem firstItem = new JMenuItem("MyExample - fun1 method");
     JMenuItem rotate = new JMenuItem("Rotate_90");
     JMenuItem grayScale = new JMenuItem("Gray Scale");
     JMenuItem edgedetection5 = new JMenuItem("edgedetection5");
     JMenuItem blur = new JMenuItem("Blur");
     JMenuItem histogram = new JMenuItem("histogram");
     JMenuItem equalize = new JMenuItem("equalize");
     firstItem.addActionListener(new ActionListener(){
            @Override
          public void actionPerformed(ActionEvent evt){fun1();}
           });
     rotate.addActionListener(new ActionListener(){
         @Override
          public void actionPerformed(ActionEvent evt){Rotate_90();}
     });
     grayScale.addActionListener(new ActionListener(){
         @Override
          public void actionPerformed(ActionEvent evt){grayScale();}
     });
     blur.addActionListener(new ActionListener(){
         @Override
          public void actionPerformed(ActionEvent evt){blur();}
     });
     edgedetection5.addActionListener(new ActionListener(){
         @Override
          public void actionPerformed(ActionEvent evt){edgedetection5();}
     });
     histogram.addActionListener(new ActionListener(){
         @Override
          public void actionPerformed(ActionEvent evt){histogram();}
     });
     equalize.addActionListener(new ActionListener(){
         @Override
          public void actionPerformed(ActionEvent evt){equalize();}
     });
     fun.add(grayScale);
      fun.add(firstItem);
      fun.add(rotate);
      fun.add(blur);
      fun.add(edgedetection5);
      fun.add(histogram);
      fun.add(equalize);
      return fun;}
  /*
   * This method handles opening an image file, breaking down the picture to a one-dimensional array and then drawing the image on the frame. 
   * You don't need to worry about this method. 
   */
    private void handleOpen(){  
     img = new ImageIcon();
     JFileChooser chooser = new JFileChooser();
      Preferences pref = Preferences.userNodeForPackage(IMP.class);
      String path = pref.get("DEFAULT_PATH", "");
      chooser.setCurrentDirectory(new File(path));
     int option = chooser.showOpenDialog(frame);
     if(option == JFileChooser.APPROVE_OPTION) {
        pic = chooser.getSelectedFile();
        pref.put("DEFAULT_PATH", pic.getAbsolutePath());
       img = new ImageIcon(pic.getPath());}
     width = img.getIconWidth();
     height = img.getIconHeight();
     originalWidth = width;
     originalHeight = height;
     
     JLabel label = new JLabel(img);
     label.addMouseListener(this);
     pixels = new int[width*height];
     results = new int[width*height];
    Image image = img.getImage(); 
     PixelGrabber pg = new PixelGrabber(image, 0, 0, width, height, pixels, 0, width );
     try{pg.grabPixels();
     }catch(InterruptedException e)
       {
          System.err.println("Interrupted waiting for pixels");
          return;}
     for(int i = 0; i<width*height; i++)
        results[i] = pixels[i];  
//     results=pixels;
     turnTwoDimensional();
     mp.removeAll();
     mp.add(label);
     mp.revalidate();}
  /*
   * The libraries in Java give a one dimensional array of RGB values for an image, I thought a 2-Dimensional array would be more usefull to you
   * So this method changes the one dimensional array to a two-dimensional. 
   */
  private void turnTwoDimensional(){
     picture = new int[height][width];
     for(int i=0; i<height; i++)
       for(int j=0; j<width; j++)
          picture[i][j] = pixels[i*width+j];
  }
  
     
  /*
   *  This method takes the picture back to the original picture
   */
  private void reset(){ 
      for(int i = 0; i<width*height; i++)
             pixels[i] = results[i];
        Image img2 = toolkit.createImage(new MemoryImageSource(width, height, pixels, 0, width));

        JLabel label2 = new JLabel(new ImageIcon(img2));
        label2.addMouseListener(this);
        mp.removeAll();
        mp.repaint();
        mp.add(label2);

        mp.revalidate();

        width = originalWidth;
        height = originalHeight;
        turnTwoDimensional();
  }

  /*
   * This method is called to redraw the screen with the new image. 
   */
  private void resetPicture(){
       for(int i=0; i<height; i++)
       for(int j=0; j<width; j++)
          pixels[i*width+j] = picture[i][j];
      Image img2 = toolkit.createImage(new MemoryImageSource(width, height, pixels, 0, width)); 
      JLabel label2 = new JLabel(new ImageIcon(img2));    
       mp.removeAll();
       mp.add(label2);
       mp.repaint();
       mp.revalidate();
        }
    /*
     * This method takes a single integer value and breaks it down doing bit manipulation to 4 individual int values for A, R, G, and B values
     */
  private int [] getPixelArray(int pixel){
      int temp[] = new int[4];
      temp[0] = (pixel >> 24) & 0xff;
      temp[1]   = (pixel >> 16) & 0xff;
      temp[2] = (pixel >>  8) & 0xff;
      temp[3]  = (pixel      ) & 0xff;
      return temp;}
    /*
     * This method takes an array of size 4 and combines the first 8 bits of each to create one integer. 
     */
  private int getPixels(int rgb[]){
         int alpha = 0;
         int rgba = (rgb[0] << 24) | (rgb[1] <<16) | (rgb[2] << 8) | rgb[3];
        return rgba;}
  public void getValue(){
      int pix = picture[colorY][colorX];
      int temp[] = getPixelArray(pix);
      System.out.println("Color value " + temp[0] + " " + temp[1] + " "+ temp[2] + " " + temp[3]);}
  /**************************************************************************************************
   * This is where you will put your methods. Every method below is called when the corresponding pulldown menu is 
   * used. As long as you have a picture open first the when your fun1, fun2, fun....etc method is called you will 
   * have a 2D array called picture that is holding each pixel from your picture. 
   *************************************************************************************************/
   /*
    * Example function that just removes all red values from the picture. 
    * Each pixel value in picture[i][j] holds an integer value. You need to send that pixel to getPixelArray the method which will return a 4 element array 
    * that holds A,R,G,B values. Ignore [0], that's the Alpha channel which is transparency, we won't be using that, but you can on your own.
    * getPixelArray will breaks down your single int to 4 ints so you can manipulate the values for each level of R, G, B. 
    * After you make changes and do your calculations to your pixel values the getPixels method will put the 4 values in your ARGB array back into a single
    * integer value so you can give it back to the program and display the new picture. 
    */
  private void equalize(){
        int[] r = new int[256];
        int[] g = new int[256];
        int[] b = new int[256];
        int[] RedPix = new int[256];
        int[] GreenPix = new int[256];
        int[] BluePix = new int[256];
        int[][] finalIMG = new int[height][width];
        for(int i = 0; i< height; i++){
            for(int j = 0; j< width; j++){

                int[] pixels = getPixelArray(picture[i][j]);
                r[pixels[1]]+=1;
                g[pixels[2]]+=1;
                b[pixels[3]]+=1;
            }
        }
        int total = 0;
        for(int i = 0; i<256; i++) {
            int number = r[i];
            total += number;
            RedPix[i] = total;
        }
        total = 0;
        for(int i = 0; i<256; i++) {
            int qtyPix = g[i];
            total += qtyPix;
            GreenPix[i] = total;
        }
        total = 0;
        for(int i = 0; i<256; i++) {
            int qtyPix = b[i];
            total += qtyPix;
            BluePix[i] = total;
        }
        int Old = 0;
        int New = 0;
        int oldRed = 0;
        int oldGreen = 0;
        int oldBlue = 0;
        int newRed=0;
        int newGreen=0;
        int newBlue=0;
        for(int i = 0; i < height; i++){
            for(int j = 0; j < width; j++){
                Old = picture[i][j];
                oldRed = getPixelArray(Old)[1];
                newRed = Math.round(((float)(RedPix[oldRed]*255))/(float)(width*height));
                oldGreen = getPixelArray(Old)[2];
                newGreen = Math.round(((float)(GreenPix[oldGreen]*255))/(float)(width*height));
                oldBlue = getPixelArray(Old)[3];
                newBlue = Math.round(((float)(BluePix[oldBlue]*255))/(float)(width*height));
                int[] newPixelArr = {255, newRed, newGreen, newBlue};
                New = getPixels(newPixelArr);
                finalIMG[i][j] = New;
            }
        }
        picture = finalIMG;
        resetPicture();
    }
  private void histogram(){
      int[] red = new int[256];
        int[] green = new int[256];
        int[] blue = new int[256];
        int redVal, greenVal, blueVal;
        for(int i = 0; i < height; i++){
            for(int j = 0; j < width; j++) {
                redVal = getPixelArray(picture[i][j])[1];
                red[redVal]++;
                greenVal = getPixelArray(picture[i][j])[2];
                green[greenVal]++;
                blueVal = getPixelArray(picture[i][j])[3];
                blue[blueVal]++;
            }
        }
        System.out.println("Red Values for my Histogram:");
        for(int i = 0; i<256; i++) {
            System.out.print(red[i] + ", ");
        }
        System.out.println();
        System.out.println("Green Values for Histogram");
        for(int i = 0; i<256; i++) {
            System.out.print(green[i] + ", ");
        }
        System.out.println();
        System.out.println("Blue Values for Histogram");
        for(int i = 0; i<256; i++){
            System.out.print(blue[i] + ", ");
        }
        System.out.println();

        JFrame redFrame = new JFrame("Red");
        redFrame.setSize(305, 600);
        redFrame.setLocation(500, 0);
        JFrame greenFrame = new JFrame("Green");
        greenFrame.setSize(305, 600);
        greenFrame.setLocation(850, 0);
        JFrame blueFrame = new JFrame("blue");
        blueFrame.setSize(305, 600);
        blueFrame.setLocation(1150, 0);
        redPanel = new MyPanel(red);
        greenPanel = new MyPanel(green);
        bluePanel = new MyPanel(blue);
        redFrame.getContentPane().add(redPanel, BorderLayout.CENTER);
        redFrame.setVisible(true);
        greenFrame.getContentPane().add(greenPanel, BorderLayout.CENTER);
        greenFrame.setVisible(true);
        blueFrame.getContentPane().add(bluePanel, BorderLayout.CENTER);
        blueFrame.setVisible(true);
        start.setEnabled(true);
        redPanel.paintComponent(gc);
        bluePanel.paintComponent(gc);
        greenPanel.paintComponent(gc);
  }
  private void edgedetection5(){
      blur();
      int [][] temp = new int[height][width];
      int r,g,b;
 for (int i = 2; i < height - 2; i++) {
            for (int j = 2; j < width - 2; j++) {
                int center = getPixelArray(picture[i][j])[2];
                int topAndBottom = 0;
                for (int k = j - 2; k < j + 3; k++) {
                    topAndBottom = topAndBottom - getPixelArray(picture[i - 2][k])[2];
                    topAndBottom = topAndBottom - getPixelArray(picture[i + 2][k])[2];
                }
                int sides = 0;
                for (int l = i - 1; l < i + 2; l++) {
                    sides = sides - getPixelArray(picture[l][j - 2])[2];
                    sides = sides - getPixelArray(picture[l][j + 2])[2];
                }
                int result = topAndBottom + sides + (center*16);
                int[] rgbArray = new int[4];
                int newColor = 0;
                if (result >= 55) {
                    newColor = 255;
                }
                rgbArray = getPixelArray(picture[i][j]);
                for (int z = 1; z < 4; z++) {
                    rgbArray[z] = newColor;
                }
                temp[i][j] = getPixels(rgbArray);
            }
        }
       
       picture = temp;
        resetPicture();
         
  }
  private void blur(){
      int[][] temp = new int[height][width];
        for(int i=1; i<height-1; i++) {
            for (int j = 1; j < width-1; j++) {
                int row1 = (getPixelArray(picture[i-1][j-1]))[2] + (getPixelArray(picture[i-1][j]))[2] + (getPixelArray(picture[i-1][j+1]))[2];
                int row2 = (getPixelArray(picture[i][j-1]))[2] + (getPixelArray(picture[i][j]))[2] + (getPixelArray(picture[i][j+1]))[2];
                int row3 = (getPixelArray(picture[i+1][j-1]))[2] + (getPixelArray(picture[i+1][j]))[2] + (getPixelArray(picture[i+1][j+1]))[2];
                int average = (row1 + row2 + row3)/9;
                int[] rgbArray = new int[4];
                rgbArray = getPixelArray(picture[i][j]);
                for(int p = 1; p < 4; p++){
                    rgbArray[p] = average;
                }
                temp[i][j] = getPixels(rgbArray);
            }
        }    picture = temp;
       resetPicture();
  }
    private void Rotate_90(){
        System.out.println("height: "+ height);
        System.out.println("witdh: "+ width);
         int rotatePic[][] = new int[width][height];
        for(int i=0; i<width; i++){
       for(int j=0; j<height; j++){   
          rotatePic[i][j] = picture[height-1-j][i];  
        }}
        int temp = width;
       width = height;
       height = temp;
        picture = rotatePic;
       resetPicture();
    }  
    
   private void grayScale(){
        int r,g,b;
       for(int i=0; i<height; i++)
       for(int j=0; j<width; j++){   
          int rgbArray[] = new int[4];   
          rgbArray = getPixelArray(picture[i][j]);
          r = rgbArray[1];
          g = rgbArray[2];
          b = rgbArray[3];
          int avg = (int) (((0.21*r)+(0.72*g)+(0.07*b))/3);
           rgbArray[1] = avg;
           rgbArray[2] = avg;
           rgbArray[3] = avg;
           picture[i][j] = getPixels(rgbArray);
} resetPicture();
            }

  private void fun1()
  {  
    for(int i=0; i<height; i++)
       for(int j=0; j<width; j++)
       {   
          int rgbArray[] = new int[4];   
          //get three ints for R, G and B
          rgbArray = getPixelArray(picture[i][j]);
           rgbArray[1] = 0;
           //take three ints for R, G, B and put them back into a single int
           picture[i][j] = getPixels(rgbArray);} resetPicture();}
  private void quit()
  {System.exit(0);}
    @Override
   public void mouseEntered(MouseEvent m){}
    @Override
   public void mouseExited(MouseEvent m){}
    @Override
   public void mouseClicked(MouseEvent m){
        colorX = m.getX();
        colorY = m.getY();
        System.out.println(colorX + "  " + colorY);
        getValue();
        start.setEnabled(true);}
    @Override
   public void mousePressed(MouseEvent m){}
    @Override
   public void mouseReleased(MouseEvent m){}
   
   public static void main(String [] args)
   {IMP imp = new IMP();}
 
}