import java.io.IOException;
import java.nio.ByteBuffer;

public class WrapBuffer {
  public void pattern(byte[] result) throws IOException {
  	ByteBuffer buffer = ByteBuffer.wrap(result); // <-- implicitly flips
	  buffer.get();
  }
}