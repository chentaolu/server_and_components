package JSON;

import java.util.HashMap;
import java.util.Map;

public class makeJSON {
	public Map<String, String> map = new HashMap<String, String>();
	
	public void addKeyAndValue(String key, String value) {
		this.map.put(key, value);
	}
	
	public String searchByKey(String key) {
		return map.get(key);
	}
}